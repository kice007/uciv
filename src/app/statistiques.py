"""Calculs des pages Statistiques et Sécurité de l'administration (les données viennent de app/mesure.py)."""
from datetime import datetime, time, timedelta

from django.db.models import Avg, Count, Max
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import EvenementSecurite, Visite

PERIODES = (7, 30, 90)
PERIODE_PAR_DEFAUT = 30


def jours_demandes(valeur):
    """Nombre de jours demandé dans l'adresse (?jours=7), limité aux périodes proposées."""
    try:
        jours = int(valeur)
    except (TypeError, ValueError):
        return PERIODE_PAR_DEFAUT
    return jours if jours in PERIODES else PERIODE_PAR_DEFAUT


def _debut(jours):
    premier_jour = timezone.localdate() - timedelta(days=jours - 1)
    return timezone.make_aware(datetime.combine(premier_jour, time.min))


def duree_texte(secondes):
    """« 2 min 14 s », « 45 s » ou « — » quand aucune durée n'a été mesurée."""
    if not secondes:
        return '—'
    secondes = int(round(secondes))
    minutes, reste = divmod(secondes, 60)
    return f'{minutes} min {reste:02d} s' if minutes else f'{reste} s'


def _hauteur(valeur, maximum):
    return round(100 * valeur / maximum) if maximum else 0


def _jours(jours):
    premier = _debut(jours).date()
    return [premier + timedelta(days=i) for i in range(jours)]


def _legende(serie):
    """Trois repères sous le graphique : premier jour, milieu, dernier jour."""
    if not serie:
        return []
    return [serie[0]['date'], serie[len(serie) // 2]['date'], serie[-1]['date']]


def statistiques_visites(jours):
    visites = Visite.objects.filter(date__gte=_debut(jours))
    par_jour = {ligne['jour']: ligne for ligne in
                visites.annotate(jour=TruncDate('date')).values('jour')
                .annotate(vues=Count('id'), visiteurs=Count('visiteur', distinct=True))}
    serie = [{'date': jour, 'vues': par_jour.get(jour, {}).get('vues', 0),
              'visiteurs': par_jour.get(jour, {}).get('visiteurs', 0)} for jour in _jours(jours)]
    maximum = max((j['vues'] for j in serie), default=0)
    for jour in serie:
        jour['h_vues'], jour['h_visiteurs'] = _hauteur(jour['vues'], maximum), _hauteur(jour['visiteurs'], maximum)

    vues = sum(j['vues'] for j in serie)
    visiteurs = sum(j['visiteurs'] for j in serie)     # visiteurs uniques de chaque jour, additionnés
    duree_moyenne = visites.exclude(duree__isnull=True).aggregate(m=Avg('duree'))['m']

    pages = [{'chemin': p['chemin'], 'vues': p['vues'], 'duree': duree_texte(p['duree']),
              'largeur': 0} for p in
             visites.values('chemin').annotate(vues=Count('id'), duree=Avg('duree')).order_by('-vues', 'chemin')[:10]]
    for page in pages:
        page['largeur'] = _hauteur(page['vues'], pages[0]['vues'])

    provenances = [{'domaine': p['referent'] or "Accès direct (ou lien sans provenance)", 'vues': p['vues']} for p in
                   visites.values('referent').annotate(vues=Count('id')).order_by('-vues')[:8]]
    for p in provenances:
        p['largeur'] = _hauteur(p['vues'], provenances[0]['vues'])

    noms = dict(Visite.APPAREILS)
    appareils = [{'nom': noms.get(a['appareil'], a['appareil']), 'vues': a['vues'],
                  'part': _hauteur(a['vues'], vues)} for a in
                 visites.values('appareil').annotate(vues=Count('id')).order_by('-vues')]

    return {
        'serie': serie, 'legende': _legende(serie), 'vues': vues, 'visiteurs': visiteurs,
        'pages_par_visiteur': round(vues / visiteurs, 1) if visiteurs else 0,
        'duree_moyenne': duree_texte(duree_moyenne),
        'mesurees': visites.exclude(duree__isnull=True).count(),
        'pages': pages, 'provenances': provenances, 'appareils': appareils,
        'aujourdhui': Visite.objects.filter(date__gte=_debut(1)).count(),
    }


def statistiques_securite(jours):
    evenements = EvenementSecurite.objects.filter(date__gte=_debut(jours))
    libelles = dict(EvenementSecurite.TYPES)
    par_jour = {ligne['jour']: ligne['n'] for ligne in
                evenements.annotate(jour=TruncDate('date')).values('jour').annotate(n=Count('id'))}
    serie = [{'date': jour, 'n': par_jour.get(jour, 0)} for jour in _jours(jours)]
    maximum = max((j['n'] for j in serie), default=0)
    for jour in serie:
        jour['h'] = _hauteur(jour['n'], maximum)

    total = sum(j['n'] for j in serie)
    types = [{'type': t['type'], 'libelle': libelles.get(t['type'], t['type']), 'n': t['n']} for t in
             evenements.values('type').annotate(n=Count('id')).order_by('-n')]
    for t in types:
        t['largeur'] = _hauteur(t['n'], types[0]['n'])

    adresses = []
    for ligne in evenements.values('ip').annotate(n=Count('id'), dernier=Max('date')).order_by('-n', 'ip')[:10]:
        genres = sorted({libelles.get(e, e) for e in
                         evenements.filter(ip=ligne['ip']).values_list('type', flat=True).distinct()})
        adresses.append({'ip': ligne['ip'], 'n': ligne['n'], 'dernier': ligne['dernier'], 'genres': ', '.join(genres)})

    cibles = [{'chemin': c['chemin'] or '/', 'n': c['n']} for c in
              evenements.values('chemin').annotate(n=Count('id')).order_by('-n', 'chemin')[:10]]
    for c in cibles:
        c['largeur'] = _hauteur(c['n'], cibles[0]['n'])

    return {
        'serie': serie, 'legende': _legende(serie), 'total': total, 'types': types,
        'adresses': adresses, 'cibles': cibles,
        'dernieres_24h': EvenementSecurite.objects.filter(date__gte=timezone.now() - timedelta(hours=24)).count(),
        'adresses_distinctes': evenements.values('ip').distinct().count(),
        'derniers': list(evenements.order_by('-date')[:25]),
    }
