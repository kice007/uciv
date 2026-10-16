"""Contenu de départ : reprend les textes de la maquette pour que les pages ne soient pas vides.

Les fiches marquées « modèle » (opportunités et ressources) sont des emplacements : l'équipe les remplace
ou les dépublie depuis l'administration. Les valeurs des indicateurs restent vides tant qu'elles ne sont pas vérifiées.
"""
import datetime

from django.db import migrations

IMG = 'app/assets/img/'

ARTICLES = [
    dict(titre="UCIV et PAIPRO-JEUNES s'associent pour l'insertion des jeunes",
         slug='uciv-et-paipro-jeunes-s-associent-pour-l-insertion-des-jeunes',
         categorie='partenariats', theme='orange', meta='Insertion professionnelle',
         chapo="À la fin des Go du Digital, les participantes sans emploi qui le souhaitent bénéficient "
               "d'un suivi vers l'insertion professionnelle.",
         corps="!! À la fin des Go du Digital, les participantes sans emploi qui souhaitent un accompagnement "
               "bénéficient désormais d'un suivi vers l'insertion professionnelle.\n\n"
               "[Paragraphe d'introduction : le contexte, la date, le lieu, les personnes impliquées.]\n\n"
               "## Un partenariat au service de l'emploi\n\n"
               "[Paragraphe de développement : ce qui s'est passé, ce que les jeunes ont appris ou réalisé.]\n\n"
               "> « Chaque engagement peut devenir une expérience. Chaque expérience peut devenir une compétence. »\n"
               "— [Nom], [rôle]\n\n"
               "[Paragraphe : les résultats, les chiffres clés de l'activité s'ils sont disponibles.]\n\n"
               "## Et après ?\n\n- [Point clé]\n- [Point clé]\n- [Point clé]\n\n"
               "[Conclusion : la suite, le prochain rendez-vous, comment s'engager.]",
         temps_lecture=4, a_la_une=True, date=datetime.date(2026, 10, 12),
         image=IMG + 'partenariat-paipro.jpg',
         image_alt="Poignée de main lors de la signature entre UCIV et PAIPRO-JEUNES.",
         image_legende="Signature de la convention entre UCIV et PAIPRO-JEUNES. Crédit : UCIV."),
    dict(titre='UCIV Leadership : la conférence de lancement au format TEDx',
         slug='uciv-leadership-la-conference-de-lancement-au-format-tedx',
         categorie='leadership', theme='jaune', meta='Octobre 2026',
         chapo="UCIV Leadership lance son réseau avec une conférence au format TEDx, à l'American Corner.",
         date=datetime.date(2026, 10, 10), image=IMG + 'affiche-leadership-jaune.jpg',
         image_alt="Affiche d'UCIV Leadership : une jeune femme lève les poings."),
    dict(titre='Des rencontres pour construire de nouvelles collaborations',
         slug='des-rencontres-pour-construire-de-nouvelles-collaborations',
         categorie='activites', theme='vert', meta='Rencontre',
         chapo="UCIV multiplie les rencontres pour construire de nouvelles collaborations.",
         date=datetime.date(2026, 10, 8), image=IMG + 'rencontre-galerie.jpg',
         image_alt='Deux hommes posent devant un tableau dans une galerie.'),
    dict(titre='Les Go du Digital : la prochaine édition se prépare',
         slug='les-go-du-digital-la-prochaine-edition-se-prepare',
         categorie='programmes', theme='orange', meta='Inscriptions',
         chapo="Les inscriptions à la prochaine édition des Go du Digital seront annoncées prochainement.",
         date=datetime.date(2026, 10, 6), image=IMG + 'go-du-digital.jpg',
         image_alt='Une jeune femme se filme avec son téléphone pendant un atelier.'),
    dict(titre="« La Reine du Digital » : le parcours d'une lauréate",
         slug='la-reine-du-digital-le-parcours-d-une-laureate',
         categorie='temoignages', theme='brun', meta='Portrait',
         chapo="Le parcours d'une lauréate de la compétition « La Reine du Digital ».",
         date=datetime.date(2026, 10, 4), image=IMG + 'go-du-digital.jpg',
         image_alt='Une jeune femme se filme avec son téléphone pendant un atelier.'),
    dict(titre="Experience Lab : apprendre à présenter son parcours",
         slug='experience-lab-apprendre-a-presenter-son-parcours',
         categorie='employabilite', theme='profond', meta='Atelier',
         chapo="Un atelier Experience Lab pour apprendre à mieux se présenter.",
         date=datetime.date(2026, 10, 3), image=IMG + 'experience-lab.jpg',
         image_alt='Un jeune homme présente son parcours devant un petit groupe.'),
    dict(titre="Sur le terrain avec les volontaires d'UCIV",
         slug='sur-le-terrain-avec-les-volontaires-d-uciv',
         categorie='engagement', theme='vert', meta='Volontariat',
         chapo="Rencontre avec les volontaires d'UCIV lors d'une action de terrain.",
         date=datetime.date(2026, 10, 1), image=IMG + 'volontaires-terrain.jpg',
         image_alt="De jeunes volontaires en tee-shirt orange lors d'une action de terrain."),
    # « Nos histoires » (page Notre impact)
    dict(titre='La lauréate de « La Reine du Digital »', slug='histoire-la-laureate-de-la-reine-du-digital',
         categorie='portraits', etiquette='Les Go du Digital', theme='orange', meta='Portrait', histoire=True,
         chapo="[Nom de la lauréate] — ce que l'expérience lui a apporté, en deux phrases.",
         date=datetime.date(2026, 9, 28), image=IMG + 'go-du-digital.jpg',
         image_alt='Une jeune femme se filme avec son téléphone pendant un atelier.'),
    dict(titre="Portrait d'un volontaire", slug='histoire-portrait-d-un-volontaire',
         categorie='portraits', etiquette='Volontariat', theme='vert', meta='Sur le terrain', histoire=True,
         chapo="Les compétences développées au fil des missions, en deux phrases.",
         date=datetime.date(2026, 9, 27), image=IMG + 'volontaires-terrain.jpg',
         image_alt="De jeunes volontaires en tee-shirt orange lors d'une action de terrain."),
    dict(titre="Parcours d'un participant", slug='histoire-parcours-d-un-participant',
         categorie='employabilite', etiquette='Employabilité', theme='profond', meta='Insertion', histoire=True,
         chapo="Comment l'expérience UCIV est devenue une opportunité, en deux phrases.",
         date=datetime.date(2026, 9, 26), image=IMG + 'experience-lab.jpg',
         image_alt='Un jeune homme présente son parcours devant un petit groupe.'),
]

INDICATEURS = ['Jeunes mobilisés', 'Volontaires', 'Programmes réalisés', 'Participants formés',
               'Partenaires', 'Projets réalisés']

OPPORTUNITES = [
    ('volontariat', 'Intitulé de la mission de volontariat', 'UCIV'),
    ('formations', "Intitulé de la formation ou de l'atelier", 'UCIV'),
    ('stages', 'Intitulé du stage', 'Partenaire'),
    ('emploi', 'Intitulé du poste', 'Partenaire'),
    ('appels', 'Nom du programme, concours ou initiative', 'UCIV ou partenaire'),
    ('formations', "Intitulé de la formation ou de l'atelier", 'Partenaire'),
]

RESSOURCES = [
    ('guide', 'employabilite', 'Titre du guide', 'Format PDF · nombre de pages'),
    ('manuel', 'volontariat', 'Titre du manuel', 'Format PDF · nombre de pages'),
    ('support', 'numerique', 'Titre du support de formation', 'Format · séance associée'),
    ('article', 'leadership', "Titre de l'article", 'Temps de lecture'),
    ('video', 'numerique', 'Titre de la vidéo', 'Durée de la vidéo'),
    ('podcast', 'leadership', "Titre de l'épisode", "Durée de l'épisode"),
    ('guide', 'volontariat', 'Titre du guide', 'Format PDF · nombre de pages'),
    ('support', 'employabilite', 'Titre du support de formation', 'Format · séance associée'),
]


def charger(apps, schema_editor):
    Article = apps.get_model('app', 'Article')
    Indicateur = apps.get_model('app', 'Indicateur')
    Opportunite = apps.get_model('app', 'Opportunite')
    Ressource = apps.get_model('app', 'Ressource')
    for donnees in ARTICLES:
        donnees = dict(donnees)
        date = donnees.pop('date')
        Article.objects.get_or_create(slug=donnees['slug'], defaults=dict(donnees, date_publication=date, publish=True))
    for ordre, libelle in enumerate(INDICATEURS, start=1):
        Indicateur.objects.get_or_create(libelle=libelle, defaults=dict(ordre=ordre, publish=True))
    # Créées dans l'ordre inverse : l'affichage trie du plus récent au plus ancien.
    for categorie, intitule, source in reversed(OPPORTUNITES):
        Opportunite.objects.create(categorie=categorie, intitule=intitule, source=source, modele=True, publish=True)
    for type_, theme, titre, meta in reversed(RESSOURCES):
        Ressource.objects.create(type=type_, theme=theme, titre=titre, meta=meta, modele=True, publish=True)


def supprimer(apps, schema_editor):
    apps.get_model('app', 'Article').objects.filter(slug__in=[a['slug'] for a in ARTICLES]).delete()
    apps.get_model('app', 'Indicateur').objects.filter(libelle__in=INDICATEURS).delete()
    apps.get_model('app', 'Opportunite').objects.filter(modele=True).delete()
    apps.get_model('app', 'Ressource').objects.filter(modele=True).delete()


class Migration(migrations.Migration):
    dependencies = [('app', '0004_article_indicateur_opportunite_ressource')]
    operations = [migrations.RunPython(charger, supprimer)]
