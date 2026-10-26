from django.core import mail
from django.utils import timezone
from django.core.cache import cache
from django.test import TestCase as TestCaseDjango, override_settings
from django.urls import reverse

from django.contrib.auth.models import User

from . import content
from .models import (
    Abonne, Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)


class TestCase(TestCaseDjango):
    """TestCase de Django, avec les compteurs du limiteur de débit remis à zéro avant chaque test."""

    def setUp(self):
        super().setUp()
        cache.clear()


class HomePageTests(TestCase):
    def test_home_renders(self):
        response = self.client.get(reverse('app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/index.html')

    def test_home_shows_key_content(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, "Une Côte d'Ivoire")
        self.assertContains(response, 'Les Go du Digital')
        self.assertContains(response, 'UCIV Leadership')
        self.assertContains(response, 'Experience Lab')
        self.assertContains(response, 'organisationuciv@gmail.com')

class UcivLeadershipPageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('app:uciv_leadership'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/uciv_leadership.html')

    def test_page_shows_key_content(self):
        response = self.client.get(reverse('app:uciv_leadership'))
        self.assertContains(response, 'Un réseau. Un engagement.')
        self.assertContains(response, '30 à 50 membres')
        self.assertContains(response, 'Membre Aspirant')
        self.assertContains(response, 'cinq engagements')
        self.assertContains(response, 'Conférence de lancement')

    def test_launch_date_is_24_october(self):
        response = self.client.get(reverse('app:uciv_leadership'))
        self.assertContains(response, '24 octobre 2026 · American Corner')
        self.assertContains(response, 'Heure à confirmer')
        self.assertContains(self.client.get(reverse('app:home')), '24 octobre 2026')

    def test_home_links_to_leadership(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:uciv_leadership'))

    def test_lancement_montre_les_deux_affiches(self):
        reponse = self.client.get(reverse('app:uciv_leadership'))
        self.assertContains(reponse, 'affiche-leadership-orange.webp')
        self.assertContains(reponse, 'affiche-leadership-jaune.webp')


class QuiSommesNousPageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('app:qui_sommes_nous'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/qui_sommes_nous.html')

    def test_page_shows_key_content(self):
        response = self.client.get(reverse('app:qui_sommes_nous'))
        self.assertContains(response, 'Notre ambition')
        self.assertContains(response, 'Former une génération de jeunes engagés')
        self.assertContains(response, 'en six mots')
        self.assertContains(response, 'Solidarité')
        self.assertContains(response, 'Marshall Kouamé')

    def test_home_links_to_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:qui_sommes_nous'))

class NosProgrammesPageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('app:nos_programmes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/nos_programmes.html')

    def test_page_shows_key_content(self):
        response = self.client.get(reverse('app:nos_programmes'))
        self.assertContains(response, 'Une même logique')
        self.assertContains(response, 'Les Go du Digital')
        self.assertContains(response, 'UCIV Leadership')
        self.assertContains(response, 'Experience Lab')
        self.assertContains(response, "D'autres programmes à venir")

    def test_links_to_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:nos_programmes'))
        response = self.client.get(reverse('app:uciv_leadership'))
        self.assertContains(response, reverse('app:nos_programmes'))

class GoDuDigitalPageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('app:go_du_digital'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/go_du_digital.html')

    def test_page_shows_key_content(self):
        response = self.client.get(reverse('app:go_du_digital'))
        self.assertContains(response, 'Les Go')
        self.assertContains(response, 'Quatre volets')
        self.assertContains(response, 'Sécurité Numérique')
        self.assertContains(response, 'La Reine')
        self.assertContains(response, 'BonixUp')

    def test_programmes_page_links_to_it(self):
        response = self.client.get(reverse('app:nos_programmes'))
        self.assertContains(response, reverse('app:go_du_digital'))

class ExperienceLabPageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('app:experience_lab'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/experience_lab.html')

    def test_page_shows_key_content(self):
        response = self.client.get(reverse('app:experience_lab'))
        self.assertContains(response, 'Know yourself')
        self.assertContains(response, "qui l&#x27;on est")
        self.assertContains(response, 'Définir leur positionnement')
        self.assertContains(response, 'Mieux te connaître')

    def test_programmes_page_links_to_it(self):
        response = self.client.get(reverse('app:nos_programmes'))
        self.assertContains(response, reverse('app:experience_lab'))

class EquipePageTests(TestCase):
    def test_page_renders(self):
        response = self.client.get(reverse('app:equipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/equipe.html')

    def test_page_shows_key_content(self):
        response = self.client.get(reverse('app:equipe'))
        self.assertContains(response, 'Les femmes et les hommes')
        self.assertContains(response, 'Marshall')
        self.assertContains(response, 'Aïssata Ouattara')
        self.assertContains(response, 'Martine Boa')
        self.assertContains(response, 'Emmanuel Fieni Kouassi')
        self.assertContains(response, 'Envie de rejoindre')

    def test_qui_sommes_nous_links_to_it(self):
        response = self.client.get(reverse('app:qui_sommes_nous'))
        self.assertContains(response, reverse('app:equipe'))

class EngagementPageTests(TestCase):
    def donnees(self, **extra):
        data = {
            'nom': 'Aya Konan', 'email': 'aya@exemple.com', 'telephone': '+225 01 02 03 04',
            'choix': 'volontaire', 'competences': ['Graphisme', 'Audiovisuel'],
            'message': 'Disponible le week-end.',
        }
        data.update(extra)
        return data

    def test_page_renders(self):
        response = self.client.get(reverse('app:engagement'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/engagement.html')
        self.assertContains(response, 'Trois façons de nous rejoindre')
        self.assertContains(response, 'Dis-nous comment')

    def test_choice_is_prefilled_from_query(self):
        response = self.client.get(reverse('app:engagement') + '?choix=competences')
        self.assertContains(response, 'value="competences" checked')

    def test_valid_submission_is_saved(self):
        response = self.client.post(reverse('app:engagement'), self.donnees())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SoumissionEngagement.objects.count(), 1)
        soumission = SoumissionEngagement.objects.get()
        self.assertEqual(soumission.nom, 'Aya Konan')
        self.assertEqual(soumission.choix, 'volontaire')
        self.assertEqual(soumission.competences, 'Graphisme, Audiovisuel')

    def test_invalid_submission_shows_errors(self):
        response = self.client.post(reverse('app:engagement'), self.donnees(email='pas-un-email', choix=''))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SoumissionEngagement.objects.count(), 0)
        self.assertContains(response, 'eng-erreur')

    def test_honeypot_blocks_robots(self):
        response = self.client.post(reverse('app:engagement'), self.donnees(site_web='http://spam'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SoumissionEngagement.objects.count(), 0)

    def test_header_links_to_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:engagement'))


    @override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.test')
    def test_team_is_notified_by_email(self):
        self.client.post(reverse('app:engagement'), self.donnees())
        self.assertEqual(len(mail.outbox), 2)   # notification à l'équipe, puis accusé de réception au visiteur
        self.assertEqual(mail.outbox[0].to, ['equipe@exemple.test'])
        self.assertIn('Aya Konan', mail.outbox[0].alternatives[0][0])
        self.assertEqual(mail.outbox[1].to, ['aya@exemple.com'])
        self.assertEqual(mail.outbox[1].reply_to, ['equipe@exemple.test'])
        self.assertIn('Bonjour Aya Konan', mail.outbox[1].alternatives[0][0])
        self.assertIn('Disponible le week-end.', mail.outbox[1].alternatives[0][0])   # rappel du message

class PartenairesPageTests(TestCase):
    def donnees(self, **extra):
        data = {
            'nom': 'Kouadio Yao', 'organisation': 'Entreprise Test', 'email': 'yao@test.ci',
            'telephone': '+225 05 06 07 08', 'type_collaboration': 'Sponsoring',
            'message': 'Nous aimerions soutenir vos programmes.',
        }
        data.update(extra)
        return data

    def test_page_renders(self):
        response = self.client.get(reverse('app:partenaires'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/partenaires.html')
        self.assertContains(response, 'Ensemble, créons')
        self.assertContains(response, 'Nous sommes')
        self.assertContains(response, 'Projets communs')
        self.assertContains(response, 'ONG Light for All CI')

    def test_valid_submission_is_saved(self):
        response = self.client.post(reverse('app:partenaires'), self.donnees())
        self.assertEqual(response.status_code, 302)
        soumission = SoumissionPartenariat.objects.get()
        self.assertEqual(soumission.organisation, 'Entreprise Test')
        self.assertEqual(soumission.type_collaboration, 'Sponsoring')

    def test_invalid_submission_shows_errors(self):
        response = self.client.post(reverse('app:partenaires'), self.donnees(email='nope', type_collaboration='???'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SoumissionPartenariat.objects.count(), 0)
        self.assertContains(response, 'eng-erreur')

    def test_honeypot_blocks_robots(self):
        response = self.client.post(reverse('app:partenaires'), self.donnees(site_web='http://spam'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SoumissionPartenariat.objects.count(), 0)

    @override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.test')
    def test_team_is_notified_by_email(self):
        self.client.post(reverse('app:partenaires'), self.donnees())
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ['equipe@exemple.test'])
        self.assertEqual(mail.outbox[1].to, ['yao@test.ci'])
        self.assertIn('votre proposition de partenariat', mail.outbox[1].alternatives[0][0])

    def test_home_links_to_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:partenaires'))

class ContactPageTests(TestCase):
    def donnees(self, **extra):
        data = {
            'nom': 'Awa Traoré', 'email': 'awa@exemple.ci', 'telephone': '+225 07 00 00 00',
            'organisation': '', 'objet': 'Presse-média', 'message': 'Bonjour, une question.',
        }
        data.update(extra)
        return data

    def test_page_renders(self):
        response = self.client.get(reverse('app:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/contact.html')
        self.assertContains(response, 'Parlons-')
        self.assertContains(response, 'Coordonnées officielles')
        self.assertContains(response, '+225 07 07 722 078')
        self.assertContains(response, 'organisationuciv@gmail.com')

    def test_valid_submission_is_saved(self):
        response = self.client.post(reverse('app:contact'), self.donnees())
        self.assertEqual(response.status_code, 302)
        soumission = SoumissionContact.objects.get()
        self.assertEqual(soumission.objet, 'Presse-média')
        self.assertEqual(soumission.organisation, '')

    def test_invalid_submission_shows_errors(self):
        response = self.client.post(reverse('app:contact'), self.donnees(objet='???', message=''))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SoumissionContact.objects.count(), 0)
        self.assertContains(response, 'eng-erreur')

    def test_honeypot_blocks_robots(self):
        response = self.client.post(reverse('app:contact'), self.donnees(site_web='http://spam'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SoumissionContact.objects.count(), 0)

    @override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.test')
    def test_team_is_notified_by_email(self):
        self.client.post(reverse('app:contact'), self.donnees())
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].reply_to, ['awa@exemple.ci'])
        self.assertEqual(mail.outbox[1].to, ['awa@exemple.ci'])
        self.assertEqual(mail.outbox[1].reply_to, ['equipe@exemple.test'])
        self.assertIn('Bonjour, une question.', mail.outbox[1].alternatives[0][0])

    def test_footer_links_to_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:contact'))

class ContenuModelsTests(TestCase):
    def test_article_image_url_prefers_static_path(self):
        article = Article.objects.create(
            titre='Un article', slug='un-article', categorie='activites',
            date_publication='2026-10-01', image='app/assets/img/groupe-nb.webp',
        )
        self.assertTrue(article.image_url.split('?')[0].endswith('app/assets/img/groupe-nb.webp'))
        self.assertEqual(str(article), 'Un article')

    def test_article_without_image_has_empty_url(self):
        article = Article.objects.create(
            titre='Sans image', slug='sans-image', categorie='portraits', date_publication='2026-10-01',
        )
        self.assertEqual(article.image_url, '')

    def test_ressource_url_uses_link_without_file(self):
        ressource = Ressource.objects.create(titre='Guide', type='guide', theme='leadership', lien='https://exemple.ci/guide.pdf')
        self.assertEqual(ressource.url, 'https://exemple.ci/guide.pdf')

    def test_new_content_is_unpublished_by_default(self):
        opportunite = Opportunite.objects.create(categorie='stages', intitule='Stage test')
        indicateur = Indicateur.objects.create(libelle='Volontaires')
        self.assertFalse(opportunite.publish)
        self.assertFalse(indicateur.publish)
        self.assertIsNone(indicateur.valeur)

class PagesDeContenuTests(TestCase):
    def test_opportunites_page_lists_published_cards(self):
        response = self.client.get(reverse('app:opportunites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/layout/opportunites.html')
        self.assertContains(response, 'Les opportunités qui peuvent')
        self.assertContains(response, 'Intitulé de la mission de volontariat')
        self.assertContains(response, 'emplacements')

    def test_opportunites_filter_and_unpublished(self):
        Opportunite.objects.create(categorie='stages', intitule='Stage secret')
        publie = Opportunite.objects.create(categorie='stages', intitule='Stage communication', publish=True)
        response = self.client.get(reverse('app:opportunites') + '?categorie=stages')
        self.assertContains(response, publie.intitule)
        self.assertNotContains(response, 'Stage secret')
        self.assertNotContains(response, 'Intitulé de la mission de volontariat')

    def test_actualites_page_has_featured_and_cards(self):
        response = self.client.get(reverse('app:actualites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lst-une')
        self.assertContains(response, "UCIV et PAIPRO-JEUNES s&#x27;associent")
        self.assertContains(response, 'Sur le terrain avec les volontaires')
        self.assertNotContains(response, 'Portrait d&#x27;un volontaire')

    def test_actualites_filter_by_category(self):
        response = self.client.get(reverse('app:actualites') + '?categorie=leadership')
        self.assertContains(response, 'conférence de lancement')
        self.assertNotContains(response, 'Des rencontres pour construire')

    def test_actualites_pagination(self):
        for n in range(8):
            Article.objects.create(titre=f'Article {n}', slug=f'article-{n}', categorie='activites',
                                   date_publication='2026-09-01', publish=True)
        response = self.client.get(reverse('app:actualites'))
        self.assertContains(response, 'lst-pagination')
        response = self.client.get(reverse('app:actualites') + '?page=2')
        self.assertEqual(response.status_code, 200)

    def test_article_page_renders_structured_body(self):
        article = Article.objects.get(slug='uciv-et-paipro-jeunes-s-associent-pour-l-insertion-des-jeunes')
        response = self.client.get(reverse('app:article', args=[article.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'art-chapo')
        self.assertContains(response, 'Un partenariat au service de l&#x27;emploi')
        self.assertContains(response, 'art-citation')
        self.assertContains(response, 'art-points')
        self.assertContains(response, 'À lire')

    def test_unpublished_article_is_404(self):
        Article.objects.create(titre='Brouillon', slug='brouillon', categorie='activites', date_publication='2026-10-01')
        self.assertEqual(self.client.get(reverse('app:article', args=['brouillon'])).status_code, 404)

    def test_body_filter_escapes_html(self):
        from .templatetags.custom_tags import corps_article
        html = corps_article('<script>alert(1)</script>\n\n## Titre <b>')
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)

    def test_impact_page(self):
        response = self.client.get(reverse('app:impact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Des actions. Des expériences.')
        self.assertContains(response, 'Jeunes mobilisés')
        self.assertContains(response, '000')
        self.assertContains(response, 'Au-delà des chiffres')
        self.assertContains(response, 'Parcours d&#x27;un participant')

    def test_impact_shows_verified_value(self):
        Indicateur.objects.filter(libelle='Volontaires').update(valeur=128)
        self.assertContains(self.client.get(reverse('app:impact')), '128')

    def test_ressources_page_and_filters(self):
        response = self.client.get(reverse('app:ressources'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apprendre. S&#x27;informer.')
        self.assertContains(response, 'Titre de la vidéo')
        response = self.client.get(reverse('app:ressources') + '?type=video&theme=numerique')
        self.assertContains(response, 'Titre de la vidéo')
        self.assertNotContains(response, 'Titre du guide')
        response = self.client.get(reverse('app:ressources') + '?type=podcast&theme=volontariat')
        self.assertContains(response, 'Aucune ressource')

    def test_home_uses_database_articles_and_indicators(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:article', args=['uciv-et-paipro-jeunes-s-associent-pour-l-insertion-des-jeunes']))
        self.assertContains(response, reverse('app:actualites'))

    def test_navigation_links_to_new_pages(self):
        response = self.client.get(reverse('app:home'))
        for nom in ('opportunites', 'actualites', 'impact', 'ressources'):
            self.assertContains(response, reverse('app:' + nom))


class AdministrationTests(TestCase):
    def connecter(self):
        from django.contrib.auth import get_user_model
        get_user_model().objects.create_superuser('equipe', 'equipe@exemple.ci', 'mot-de-passe-solide',
                                                  first_name='Emmanuel')
        self.client.login(username='equipe', password='mot-de-passe-solide')

    def test_login_page_wears_uciv_branding(self):
        response = self.client.get('/back-office/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'app/assets/css/admin.css')
        self.assertContains(response, 'Espace <em>équipe.</em>')
        self.assertContains(response, 'Accès réservé à l\'équipe UCIV.')
        self.assertContains(response, 'Administration UCIV')
        self.assertNotContains(response, 'uciv-lateral')

    def test_dashboard_greets_user_and_shows_key_figures(self):
        self.connecter()
        Article.objects.create(titre='Publié', slug='publie', categorie='activites', date_publication='2026-10-01',
                               publish=True)
        Abonne.objects.create(email='lecteur@exemple.ci')
        response = self.client.get('/back-office/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bonjour Emmanuel')
        for texte in ('Articles publiés', 'Opportunités en ligne', 'Ressources', 'Abonnés actifs', 'À faire',
                      'Raccourcis', 'Derniers contenus modifiés', 'Messages récents'):
            self.assertContains(response, texte)
        self.assertContains(response, 'fiches d&#x27;exemple')
        self.assertContains(response, 'opportunités sont des fiches d&#x27;exemple')

    def test_dashboard_data_counts(self):
        from django.template import Context, Template
        Opportunite.objects.all().delete()
        Ressource.objects.all().delete()
        Opportunite.objects.create(categorie='stages', intitule='Exemple', publish=True, modele=True)
        Opportunite.objects.create(categorie='stages', intitule='Réelle', publish=True)
        Abonne.objects.create(email='lecteur@exemple.ci')
        Abonne.objects.create(email='parti@exemple.ci', actif=False)
        donnees = Template('{% load uciv_admin %}{% tableau_de_bord as d %}{{ d.chiffres.1.valeur }}|{{ d.chiffres.1.sous }}'
                           '|{{ d.chiffres.3.valeur }}').render(Context())
        self.assertEqual(donnees, '2|dont 1 fiche d\'exemple|1'.replace("'", '&#x27;'))

    def test_sidebar_groups_and_unread_badge(self):
        self.connecter()
        SoumissionContact.objects.create(nom='Aya Koné', email='aya@exemple.ci', objet='Programme', message='Bonjour')
        SoumissionContact.objects.create(nom='Déjà lu', email='lu@exemple.ci', objet='Autre', message='Salut',
                                         publish=True)
        response = self.client.get('/back-office/app/article/')
        self.assertEqual(response.status_code, 200)
        for texte in ('Pilotage', 'Contenu du site', 'Suivi', 'Tableau de bord', 'Articles',
                      'Chiffres d&#x27;impact', 'Messages reçus', 'Abonnés', 'Voir le site'):
            self.assertContains(response, texte)
        self.assertContains(response, '<span class="uciv-nav__badge">1</span>', html=True)
        self.assertContains(response, 'uciv-nav__lien est-actif', count=1)

    def test_recent_messages_show_new_status(self):
        self.connecter()
        SoumissionContact.objects.create(nom='Aya Koné', email='aya@exemple.ci', objet='Programme', message='Bonjour')
        response = self.client.get('/back-office/')
        self.assertContains(response, 'Aya Koné')
        self.assertContains(response, 'Contact · Programme')
        self.assertContains(response, 'pastille--nouveau')
        self.assertContains(response, '1 nouveau message')

    def test_changelists_show_status_pills_and_bulk_actions(self):
        self.connecter()
        Article.objects.create(titre='Brouillon', slug='brouillon-a', categorie='activites',
                               date_publication='2026-10-01')
        publie = Article.objects.create(titre='Publié', slug='publie-a', categorie='activites',
                                        date_publication='2026-10-02', publish=True)
        Opportunite.objects.create(categorie='stages', intitule='Exemple', publish=True, modele=True)
        reponse = self.client.get('/back-office/app/article/')
        self.assertContains(reponse, 'pastille--brouillon')
        self.assertContains(reponse, 'pastille--publie')
        self.assertContains(self.client.get('/back-office/app/opportunite/'), 'Fiche d&#x27;exemple')
        self.client.post('/back-office/app/article/', {'action': 'mettre_en_brouillon', '_selected_action': [publie.pk]})
        publie.refresh_from_db()
        self.assertFalse(publie.publish)
        self.client.post('/back-office/app/article/', {'action': 'publier', '_selected_action': [publie.pk]})
        publie.refresh_from_db()
        self.assertTrue(publie.publish)

    def test_admin_pages_still_render(self):
        self.connecter()
        for url in ('/back-office/app/article/add/', '/back-office/app/opportunite/', '/back-office/app/ressource/',
                    '/back-office/app/indicateur/', '/back-office/app/abonne/', '/back-office/app/soumissionengagement/',
                    '/back-office/app/soumissionpartenariat/', '/back-office/auth/user/', '/back-office/password_change/'):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_lists_follow_the_mockup_without_django_filters(self):
        self.connecter()
        Article.objects.all().delete()
        Article.objects.create(titre='Brouillon', slug='b1', categorie='activites', date_publication='2026-10-01')
        Article.objects.create(titre='Publié', slug='p1', categorie='activites', date_publication='2026-10-02',
                               publish=True, a_la_une=True)
        reponse = self.client.get('/back-office/app/article/')
        self.assertNotContains(reponse, 'changelist-filter')
        self.assertNotContains(reponse, 'class="breadcrumbs"')
        self.assertNotContains(reponse, 'Choisir une option')
        for chip in ('Tous', 'Publiés', 'Brouillons', 'À la une', 'Nos histoires'):
            self.assertContains(reponse, chip)
        self.assertContains(reponse, 'Nouvel article')
        self.assertContains(reponse, '2 articles sur 2')
        self.assertContains(self.client.get('/back-office/app/article/?publish__exact=0'), '1 articles sur 1')
        publies = self.client.get('/back-office/app/article/?publish__exact=1')
        self.assertContains(publies, 'class="chip est-actif"')
        self.assertContains(publies, 'À la une · 3 min')

    def test_list_search_and_chips_keep_each_other(self):
        self.connecter()
        Article.objects.all().delete()
        Article.objects.create(titre='Go du Digital', slug='g1', categorie='activites', date_publication='2026-10-01',
                               publish=True)
        Article.objects.create(titre='Autre sujet', slug='a1', categorie='activites', date_publication='2026-10-02',
                               publish=True)
        reponse = self.client.get('/back-office/app/article/?q=Digital&publish__exact=1')
        self.assertContains(reponse, 'Go du Digital')
        self.assertNotContains(reponse, 'Autre sujet')
        self.assertContains(reponse, 'name="publish__exact" value="1"')

    def test_opportunity_and_resource_lists_have_their_own_filters(self):
        self.connecter()
        reponse = self.client.get('/back-office/app/opportunite/')
        for chip in ('Toutes', 'Volontariat', 'Formations', 'Stages', 'Emploi', "Fiches d&#x27;exemple"):
            self.assertContains(reponse, chip)
        self.assertContains(reponse, 'Nouvelle opportunité')
        self.assertContains(reponse, 'Date limite')
        reponse = self.client.get('/back-office/app/ressource/')
        for chip in ('Toutes', 'Guides', 'Vidéos', 'Podcasts'):
            self.assertContains(reponse, chip)
        self.assertContains(reponse, 'Nouvelle ressource')

    def test_row_menu_publishes_and_deletes(self):
        self.connecter()
        Article.objects.all().delete()
        article = Article.objects.create(titre='À publier', slug='ap', categorie='activites',
                                         date_publication='2026-10-01')
        reponse = self.client.get('/back-office/app/article/')
        self.assertContains(reponse, 'value="publier"')
        self.assertContains(reponse, reverse('admin:app_article_delete', args=[article.pk]))
        self.assertContains(reponse, 'Modifier')

    def test_article_form_is_split_in_cards_like_the_mockup(self):
        self.connecter()
        article = Article.objects.create(titre='Mon article', slug='mon-article', categorie='activites',
                                         date_publication='2026-10-01', publish=True)
        reponse = self.client.get(f'/back-office/app/article/{article.pk}/change/')
        for titre in ('Contenu', 'Repères', 'Publication', 'Image'):
            self.assertContains(reponse, f'<h2 class="formcarte__titre">{titre}</h2>', html=True)
        self.assertContains(reponse, "Modifier l&#x27;article")
        self.assertContains(reponse, 'Voir sur le site')
        self.assertContains(reponse, 'Enregistrer')
        self.assertContains(reponse, "Supprimer l&#x27;article")
        self.assertContains(reponse, 'class="bascule"', count=3)
        self.assertNotContains(reponse, 'submit-row')
        self.assertNotContains(reponse, 'Enregistrer et continuer')

    def test_new_forms_use_the_mockup_titles(self):
        self.connecter()
        self.assertContains(self.client.get('/back-office/app/opportunite/add/'), 'Nouvelle opportunité')
        self.assertContains(self.client.get('/back-office/app/opportunite/add/'), 'Brouillon')
        self.assertContains(self.client.get('/back-office/app/ressource/add/'), 'Nouvelle ressource')
        self.assertContains(self.client.get('/back-office/app/article/add/'), 'Nouvel article')

    def test_saving_a_form_with_the_save_button(self):
        self.connecter()
        reponse = self.client.post('/back-office/app/opportunite/add/', {
            'intitule': 'Mission test', 'categorie': 'stages', 'source': 'UCIV', 'structure': '', 'lieu': 'Abidjan',
            'description': '', 'date_limite': '', 'lien': '', 'publish': 'on', '_continue': '1',
        })
        self.assertEqual(reponse.status_code, 302)
        self.assertTrue(Opportunite.objects.filter(intitule='Mission test', publish=True).exists())

    def test_sidebar_matches_the_mockup(self):
        self.connecter()
        reponse = self.client.get('/back-office/')
        for texte in ('Messages reçus', 'Abonnés', "Chiffres d&#x27;impact"):
            self.assertContains(reponse, texte)
        for absent in ("Demandes d&#x27;engagement", 'Propositions de partenariat', 'Groupes'):
            self.assertNotContains(reponse, absent)

    def test_inbox_merges_the_three_forms(self):
        self.connecter()
        SoumissionContact.objects.create(nom='Mariam Traoré', email='m@exemple.ci', objet='Une question', message='Salut')
        SoumissionPartenariat.objects.create(nom='Awa Diallo', organisation='BonixUp', email='b@exemple.ci',
                                             type_collaboration='Partenariats techniques', message='Collaborons')
        SoumissionEngagement.objects.create(nom='Aya Konan', email='aya@exemple.ci', choix='volontaire',
                                            competences='Communication, Événementiel', message='Bonjour')
        reponse = self.client.get('/back-office/app/soumissioncontact/')
        self.assertContains(reponse, 'Tous (3)')
        self.assertContains(reponse, 'Nouveaux (3)')
        for texte in ('Mariam Traoré', 'BonixUp · Awa Diallo', 'Aya Konan', 'Contact · Une question',
                      'Partenariat · Partenariats techniques', "Je veux m&#x27;engager · Devenir volontaire"):
            self.assertContains(reponse, texte)
        engagement = self.client.get('/back-office/app/soumissioncontact/?f=engagement')
        self.assertContains(engagement, 'Aya Konan')
        self.assertNotContains(engagement, 'Mariam Traoré')
        self.assertContains(engagement, 'Répondre par e-mail')
        self.assertContains(engagement, 'mailto:aya@exemple.ci')
        self.assertContains(engagement, 'Communication, Événementiel')

    def test_inbox_can_mark_a_message_as_handled_and_back(self):
        self.connecter()
        message = SoumissionContact.objects.create(nom='Aya', email='aya@exemple.ci', objet='Autre', message='Salut')
        url = '/back-office/app/soumissioncontact/'
        reponse = self.client.post(url, {'message': f'contact-{message.pk}', 'etat': 'traite', 'f': 'tous'})
        self.assertEqual(reponse.status_code, 302)
        message.refresh_from_db()
        self.assertTrue(message.publish)
        self.assertContains(self.client.get(url), 'Remettre à traiter')
        self.client.post(url, {'message': f'contact-{message.pk}', 'etat': 'a_traiter'})
        message.refresh_from_db()
        self.assertFalse(message.publish)

    def test_inbox_ignores_unknown_message_ids(self):
        self.connecter()
        reponse = self.client.post('/back-office/app/soumissioncontact/', {'message': 'inconnu-1', 'etat': 'traite'})
        self.assertEqual(reponse.status_code, 302)
        reponse = self.client.post('/back-office/app/soumissioncontact/', {'message': 'contact-abc', 'etat': 'traite'})
        self.assertEqual(reponse.status_code, 302)

    def test_empty_inbox(self):
        self.connecter()
        self.assertContains(self.client.get('/back-office/app/soumissioncontact/'), 'Aucun message pour le moment')

    def test_subscribers_page_shows_figures_search_and_export(self):
        self.connecter()
        Abonne.objects.create(email='aya.konan@gmail.com')
        Abonne.objects.create(email='k.yao@outlook.fr')
        parti = Abonne.objects.create(email='j.kouadio@gmail.com', actif=False)
        parti.desinscrit_le = timezone.now()
        parti.save()
        reponse = self.client.get('/back-office/app/abonne/')
        for texte in ('Abonnés actifs', 'Ce mois-ci', 'Désinscrits', 'Exporter en CSV', 'aya.konan@gmail.com',
                      'Rechercher une adresse'):
            self.assertContains(reponse, texte)
        self.assertContains(reponse, 'Désinscrit le')
        self.assertContains(self.client.get('/back-office/app/abonne/?q=outlook'), 'k.yao@outlook.fr')
        self.assertNotContains(self.client.get('/back-office/app/abonne/?q=outlook'), 'aya.konan@gmail.com')
        export = self.client.get(reverse('admin:app_abonne_export'))
        contenu = export.content.decode('utf-8-sig')
        self.assertIn('aya.konan@gmail.com', contenu)
        self.assertNotIn('j.kouadio@gmail.com', contenu)

    def test_impact_figures_page_edits_values_in_the_list(self):
        self.connecter()
        Indicateur.objects.all().delete()
        vide = Indicateur.objects.create(libelle='Volontaires', ordre=1, publish=True)
        rempli = Indicateur.objects.create(libelle='Partenaires', valeur=3, ordre=2, publish=True)
        reponse = self.client.get('/back-office/app/indicateur/')
        self.assertContains(reponse, "Chiffres d&#x27;impact")
        self.assertContains(reponse, 'Un chiffre laissé vide')
        self.assertContains(reponse, "N'affichez que des chiffres vérifiés")
        self.assertContains(reponse, 'placeholder="À renseigner"')
        self.assertContains(reponse, 'pastille--avenir')
        self.assertContains(reponse, 'pastille--publie')
        donnees = {'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2', 'form-MIN_NUM_FORMS': '0',
                   'form-MAX_NUM_FORMS': '1000', 'form-0-id': vide.pk, 'form-0-valeur': '42',
                   'form-1-id': rempli.pk, 'form-1-valeur': '3', '_save': 'Enregistrer'}
        self.assertEqual(self.client.post('/back-office/app/indicateur/', donnees).status_code, 302)
        vide.refresh_from_db()
        self.assertEqual(vide.valeur, 42)

    def test_other_pages_have_no_breadcrumbs_or_django_chrome(self):
        self.connecter()
        reponse = self.client.get('/back-office/app/indicateur/')
        self.assertNotContains(reponse, 'class="breadcrumbs"')
        self.assertContains(reponse, 'uciv-lateral')

    def test_unauthorized_staff_cannot_open_the_inbox(self):
        from django.contrib.auth import get_user_model
        get_user_model().objects.create_user('simple', 'simple@exemple.ci', 'mot-de-passe-solide', is_staff=True)
        self.client.login(username='simple', password='mot-de-passe-solide')
        self.assertEqual(self.client.get('/back-office/app/soumissioncontact/').status_code, 403)

    def test_fresh_content_shows_just_now(self):
        from django.template import Context, Template
        Article.objects.create(titre='Tout neuf', slug='tout-neuf', categorie='activites', date_publication='2026-10-01')
        rendu = Template('{% load uciv_admin %}{% tableau_de_bord as d %}{{ d.contenus.0.quand }}').render(Context())
        self.assertIn('instant', rendu)


class ReglagesBaseDeDonneesTests(TestCase):
    """Les réglages MySQL se vérifient dans un sous-processus : aucune connexion n'est ouverte."""

    def base(self, **env):
        import json
        import os
        import subprocess
        import sys
        from django.conf import settings
        code = "import json; from core import settings as s; print(json.dumps(s.DATABASES['default'], default=str))"
        environ = {k: v for k, v in os.environ.items() if not k.startswith('MYSQL_') and k != 'USE_MYSQL'}
        environ.update(env)
        resultat = subprocess.run([sys.executable, '-c', code], cwd=settings.BASE_DIR, env=environ,
                                  capture_output=True, text=True, check=True)
        return json.loads(resultat.stdout)

    def test_sqlite_by_default(self):
        self.assertTrue(self.base()['ENGINE'].endswith('sqlite3'))

    def test_mysql_settings_use_utf8mb4_without_forced_ssl(self):
        base = self.base(USE_MYSQL='True', MYSQL_DB='uciv', MYSQL_USER='uciv_user', MYSQL_PASSWORD='secret')
        self.assertEqual(base['ENGINE'], 'django.db.backends.mysql')
        self.assertEqual((base['NAME'], base['USER'], base['HOST'], base['PORT']), ('uciv', 'uciv_user', 'localhost', '3306'))
        self.assertEqual(base['OPTIONS']['charset'], 'utf8mb4')
        self.assertNotIn('ssl_mode', base['OPTIONS'])
        self.assertNotIn('ssl', base['OPTIONS'])
        self.assertEqual(base['CONN_MAX_AGE'], 60)

    def test_mysql_ssl_is_opt_in(self):
        base = self.base(USE_MYSQL='True', MYSQL_DB='uciv', MYSQL_USER='u', MYSQL_PASSWORD='p', MYSQL_SSL_MODE='REQUIRED')
        self.assertEqual(base['OPTIONS']['ssl_mode'], 'REQUIRED')

class ReferencementTests(TestCase):
    def html(self, nom, **params):
        reponse = self.client.get(reverse('app:' + nom), params)
        self.assertEqual(reponse.status_code, 200, nom)
        return reponse.content.decode()

    def test_every_page_has_complete_meta_tags(self):
        import re
        for nom in content.PAGES_INDEXABLES:
            html = self.html(nom)
            from html import unescape  # les apostrophes sont écrites &#x27; dans le HTML : on mesure le texte lu
            titre = unescape(re.search(r'<title>(.*?)</title>', html, re.S).group(1))
            description = unescape(re.search(r'<meta name="description" content="(.*?)">', html, re.S).group(1))
            self.assertTrue(30 <= len(titre) <= 60, f'{nom} : titre de {len(titre)} caractères')
            self.assertTrue(110 <= len(description) <= 160, f'{nom} : description de {len(description)} caractères')
            for balise in ('<link rel="canonical" href="http', '<meta name="robots" content="index, follow">',
                           '<meta property="og:title"', '<meta property="og:description"', '<meta property="og:url"',
                           '<meta property="og:image" content="http', '<meta name="twitter:card"',
                           '<meta property="og:locale" content="fr_FR">'):
                self.assertIn(balise, html, f'{nom} : {balise}')

    def test_titles_and_descriptions_are_unique(self):
        titres = [page['titre'] for page in content.SEO_PAGES.values()]
        descriptions = [page['description'] for page in content.SEO_PAGES.values()]
        self.assertEqual(len(set(titres)), len(titres))
        self.assertEqual(len(set(descriptions)), len(descriptions))

    def test_one_h1_and_alt_on_every_image(self):
        import re
        for nom in content.PAGES_INDEXABLES:
            html = self.html(nom)
            self.assertEqual(len(re.findall(r'<h1[\s>]', html)), 1, f'{nom} : un seul h1')
            for image in re.findall(r'<img\b[^>]*>', html):
                self.assertIn(' alt=', image, f'{nom} : image sans alt : {image[:80]}')

    def test_structured_data_is_valid_and_current(self):
        import json
        import re
        for nom in content.PAGES_INDEXABLES:
            html = self.html(nom)
            blocs = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
            self.assertTrue(blocs, nom)
            for bloc in blocs:
                donnees = json.loads(bloc)
                self.assertEqual(donnees['@context'], 'https://schema.org')
            for interdit in ('"FAQPage"', '"HowTo"'):
                self.assertNotIn(interdit, html, f'{nom} : type obsolète ou restreint')

    def test_home_declares_organization_and_website(self):
        import json
        import re
        html = self.html('home')
        types = [json.loads(b)['@type'] for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]
        self.assertEqual(types[:2], ['NGO', 'WebSite'])
        organisation = json.loads(re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)[0])
        self.assertEqual(organisation['founder']['name'], 'Marshall Kouamé')
        self.assertTrue(all(url.startswith('https://') for url in organisation['sameAs']))

    def test_inner_pages_have_breadcrumbs(self):
        import json
        import re
        html = self.html('go_du_digital')
        fil = next(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                   if '"BreadcrumbList"' in b)
        self.assertEqual([i['name'] for i in fil['itemListElement']], ['Accueil', 'Nos programmes', 'Les Go du Digital'])
        self.assertEqual([i['position'] for i in fil['itemListElement']], [1, 2, 3])

    def test_leadership_declares_the_launch_event(self):
        import json
        import re
        html = self.html('uciv_leadership')
        evenement = next(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                         if '"Event"' in b)
        self.assertEqual(evenement['startDate'], '2026-10-24')
        self.assertEqual(evenement['location']['name'], 'American Corner')

    def test_programs_declare_courses(self):
        for nom in ('go_du_digital', 'experience_lab'):
            self.assertIn('"@type": "Course"', self.html(nom))

    def test_article_page_has_article_markup(self):
        import json
        import re
        article = Article.objects.get(slug='uciv-et-paipro-jeunes-s-associent-pour-l-insertion-des-jeunes')
        html = self.client.get(reverse('app:article', args=[article.slug])).content.decode()
        donnees = next(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                       if '"Article"' in b)
        self.assertEqual(donnees['@type'], 'Article')
        self.assertLessEqual(len(donnees['headline']), 110)
        self.assertIn('datePublished', donnees)
        self.assertTrue(donnees['image'][0].startswith('http'))
        self.assertIn('<meta property="og:type" content="article">', html)
        self.assertIn('article:published_time', html)
        self.assertIn(f'<link rel="canonical" href="http://testserver{article.get_absolute_url()}">', html)

    def test_filtered_pages_are_not_indexed_and_keep_clean_canonical(self):
        html = self.html('actualites', categorie='leadership')
        self.assertIn('<meta name="robots" content="noindex, follow">', html)
        self.assertIn('<link rel="canonical" href="http://testserver/actualites/">', html)
        html = self.html('ressources', type='video')
        self.assertIn('noindex, follow', html)
        html = self.html('engagement', choix='volontaire')
        self.assertIn('noindex, follow', html)

    def test_pagination_page_is_indexed_with_its_own_canonical(self):
        for n in range(8):
            Article.objects.create(titre=f'Article {n}', slug=f'article-seo-{n}', categorie='activites',
                                   date_publication='2026-09-01', publish=True)
        html = self.html('actualites', page=2)
        self.assertIn('<meta name="robots" content="index, follow">', html)
        self.assertIn('<link rel="canonical" href="http://testserver/actualites/?page=2">', html)

    @override_settings(SITE_URL='https://uciv.org')
    def test_site_url_setting_fixes_canonical_host(self):
        html = self.html('contact')
        self.assertIn('<link rel="canonical" href="https://uciv.org/contact/">', html)
        self.assertIn('<meta property="og:url" content="https://uciv.org/contact/">', html)

    def test_robots_txt(self):
        reponse = self.client.get('/robots.txt')
        self.assertEqual(reponse.status_code, 200)
        self.assertEqual(reponse['Content-Type'], 'text/plain; charset=utf-8')
        texte = reponse.content.decode()
        self.assertNotIn('admin', texte.lower())    # l'adresse secrète de l'administration ne doit pas fuiter
        self.assertIn('Sitemap: http://testserver/sitemap.xml', texte)

    def test_sitemap_lists_pages_and_published_articles_only(self):
        Article.objects.create(titre='Brouillon', slug='brouillon-sitemap', categorie='activites', date_publication='2026-10-01')
        reponse = self.client.get('/sitemap.xml')
        self.assertEqual(reponse.status_code, 200)
        xml = reponse.content.decode()
        for nom in content.PAGES_INDEXABLES:
            self.assertIn(f'<loc>https://testserver{reverse("app:" + nom)}</loc>', xml, nom)
        self.assertIn('/actualites/uciv-leadership-la-conference-de-lancement-au-format-tedx/', xml)
        self.assertNotIn('brouillon-sitemap', xml)
        self.assertNotIn('<priority>', xml)
        self.assertNotIn('<changefreq>', xml)

    @override_settings(SITE_URL='https://uciv.org')
    def test_sitemap_uses_site_url(self):
        xml = self.client.get('/sitemap.xml', HTTP_HOST='www.uciv.org').content.decode()
        self.assertIn('<loc>https://uciv.org/</loc>', xml)
        self.assertNotIn('www.uciv.org', xml)
        self.assertNotIn('testserver', xml)

    def test_llms_txt(self):
        reponse = self.client.get('/llms.txt')
        self.assertEqual(reponse.status_code, 200)
        texte = reponse.content.decode()
        self.assertTrue(texte.startswith("# Une Côte d'Ivoire Volontaire (UCIV)"))
        self.assertIn('/programmes/uciv-leadership/', texte)

    def test_not_found_page_is_noindex(self):
        reponse = self.client.get('/page-qui-nexiste-pas/')
        self.assertEqual(reponse.status_code, 404)
        html = reponse.content.decode()
        self.assertIn('noindex, nofollow', html)
        self.assertIn('Cette page <em>', html)
        self.assertIn('Erreur 404', html)


class ImagesDuSiteTests(TestCase):
    def test_every_image_referenced_exists_and_is_light(self):
        import re
        from pathlib import Path
        from django.conf import settings
        dossier = Path(settings.BASE_DIR) / 'static'
        fichiers = list((Path(settings.BASE_DIR) / 'app').glob('*.py')) + list((Path(settings.BASE_DIR) / 'templates').rglob('*.html'))
        references = set()
        for fichier in fichiers:
            if fichier.name == 'tests.py':
                continue
            references |= set(re.findall(r"app/assets/img/[\w.-]+\.(?:webp|jpg|png)", fichier.read_text(encoding='utf-8')))
        self.assertTrue(references)
        for chemin in sorted(references):
            fichier = dossier / chemin
            self.assertTrue(fichier.exists(), f'image absente : {chemin}')
            self.assertLessEqual(fichier.stat().st_size / 1024, 200, f'image trop lourde : {chemin}')

    def test_site_serves_webp_photos(self):
        html = self.client.get(reverse('app:go_du_digital')).content.decode()
        self.assertIn('/static/app/assets/img/go-du-digital-couverture.webp', html)
        self.assertNotIn('.jpg"', html.split('</head>')[1].replace('og-', ''))

    def test_article_images_in_database_use_webp(self):
        for article in Article.objects.filter(image__startswith='app/assets/img/'):
            self.assertTrue(article.image.endswith(('.webp', '.jpg')), article.image)
            self.assertFalse(article.image.endswith('.png'), article.image)

class GeoTests(TestCase):
    def html(self, nom):
        return self.client.get(reverse('app:' + nom)).content.decode()

    def test_every_page_has_a_visible_faq_with_question_headings(self):
        import re
        for nom in content.PAGES_INDEXABLES:
            html = self.html(nom)
            self.assertIn('class="faq"', html, nom)
            self.assertIn('Questions fréquentes', html, nom)
            questions = re.findall(r'<div class="faq__item"[^>]*>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.S)
            self.assertGreaterEqual(len(questions), 2, nom)
            for question, reponse in questions:
                self.assertTrue(question.strip().endswith('?'), f'{nom} : {question}')
                self.assertGreaterEqual(len(reponse.split()), 12, f'{nom} : réponse trop courte à « {question} »')

    def test_faq_questions_are_unique_and_have_no_faqpage_markup(self):
        questions = [q for faq in content.FAQ.values() for q, _ in faq]
        self.assertEqual(len(questions), len(set(questions)))
        for nom in content.PAGES_INDEXABLES:
            self.assertNotIn('FAQPage', self.html(nom))

    def test_faq_facts_match_site_data(self):
        faq_lead = dict(content.FAQ['uciv_leadership'])
        self.assertIn('24 octobre 2026', faq_lead["Quand a lieu le lancement d'UCIV Leadership ?"])
        self.assertIn('30 et 50', faq_lead['Combien de membres compte la cohorte pionnière ?'])
        faq_contact = ' '.join(dict(content.FAQ['contact']).values())
        for coordonnee in ('+225 07 87 56 17 66', '+225 07 07 722 078', 'organisationuciv@gmail.com', '04 BP 2087'):
            self.assertIn(coordonnee, faq_contact)

    def test_robots_names_and_allows_ai_crawlers(self):
        texte = self.client.get('/robots.txt').content.decode()
        for robot in ('GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'PerplexityBot'):
            self.assertIn(f'User-agent: {robot}', texte)
        self.assertNotIn('Disallow', texte)
        self.assertNotIn('admin', texte.lower())
        self.assertIn('Sitemap:', texte)

    def test_llms_txt_has_key_facts_and_latest_news(self):
        texte = self.client.get('/llms.txt').content.decode()
        self.assertIn('## Faits clés', texte)
        self.assertIn('Marshall Kouamé', texte)
        self.assertIn('24 octobre 2026', texte)
        self.assertIn('## Dernières actualités', texte)
        self.assertIn('/actualites/', texte)
        self.assertIn('## Réseaux et profils', texte)

    def test_team_page_declares_people(self):
        import json
        import re
        html = self.html('equipe')
        liste = next(json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
                     if '"Person"' in b)
        noms = [e['item']['name'] for e in liste['itemListElement']]
        self.assertIn('Marshall Kouamé', noms)
        self.assertIn('Martine Boa', noms)
        self.assertEqual(len(noms), 18)   # le président et les 17 membres des trois groupes
        self.assertTrue(all(e['item']['worksFor']['@id'].endswith('/#organisation') for e in liste['itemListElement']))

    def test_collection_pages_declare_date_modified(self):
        import re
        html = self.html('actualites')
        self.assertRegex(html, r'"dateModified": "\d{4}-\d{2}-\d{2}')

    def test_article_dates_use_time_elements(self):
        article = Article.objects.get(slug='uciv-et-paipro-jeunes-s-associent-pour-l-insertion-des-jeunes')
        html = self.client.get(reverse('app:article', args=[article.slug])).content.decode()
        self.assertRegex(html, r'<time datetime="\d{4}-\d{2}-\d{2}">')


class PagesLegalesTests(TestCase):
    """Mentions légales, politique de confidentialité, conditions d'utilisation."""

    def test_les_trois_pages_repondent(self):
        for nom, titre in [('app:mentions_legales', 'Mentions'),
                           ('app:confidentialite', 'Politique de'),
                           ('app:conditions', 'Conditions')]:
            response = self.client.get(reverse(nom))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, titre)
            self.assertContains(response, 'Sur cette page')
            self.assertContains(response, 'Les autres')

    def test_texte_a_completer_signale(self):
        response = self.client.get(reverse('app:mentions_legales'))
        self.assertContains(response, '<span class="a-completer">[Nom de l&#x27;hébergeur]</span>', html=False)

    def test_pied_de_page_relie_les_pages_legales(self):
        response = self.client.get(reverse('app:home'))
        for nom in ['app:mentions_legales', 'app:confidentialite', 'app:conditions']:
            self.assertContains(response, f'href="{reverse(nom)}"')

    def test_formulaires_relient_la_politique(self):
        url = reverse('app:confidentialite')
        for nom in ['app:engagement', 'app:contact']:
            self.assertContains(self.client.get(reverse(nom)), f'href="{url}"')


class PageIntrouvableTests(TestCase):
    def test_page_404_du_site(self):
        response = self.client.get('/cette-page-n-existe-pas/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "s&#x27;est égarée.", status_code=404)
        self.assertContains(response, f'href="{reverse("app:contact")}"', status_code=404)


class NewsletterTests(TestCase):
    """Lettre d'information : inscription depuis le pied de page, désinscription, export."""

    def inscrire(self, email, depuis='/programmes/', **extra):
        donnees = {'email': email, 'suivant': depuis, **extra}
        return self.client.post(reverse('app:newsletter_inscription'), donnees)

    def test_inscription_puis_message_dans_la_carte(self):
        reponse = self.inscrire('Aya.Konan@Example.com')
        self.assertRedirects(reponse, '/programmes/#lettre', fetch_redirect_response=False)
        self.assertTrue(Abonne.objects.filter(email='aya.konan@example.com', actif=True).exists())
        page = self.client.get('/programmes/')
        self.assertContains(page, 'Merci, c&#x27;est noté !')
        # Le message ne s'affiche qu'une fois.
        self.assertNotContains(self.client.get('/programmes/'), 'Merci, c&#x27;est noté !')

    def test_adresse_deja_inscrite(self):
        Abonne.objects.create(email='aya@example.com')
        self.inscrire('aya@example.com')
        self.assertContains(self.client.get('/programmes/'), 'Vous êtes déjà inscrit·e.')
        self.assertEqual(Abonne.objects.count(), 1)

    def test_adresse_invalide(self):
        self.inscrire('aya.konan@gmail')
        page = self.client.get('/programmes/')
        self.assertContains(page, 'Saisissez une adresse e-mail valide.')
        self.assertContains(page, 'value="aya.konan@gmail"')
        self.assertFalse(Abonne.objects.exists())

    def test_champ_piege_rien_enregistre(self):
        self.inscrire('robot@example.com', site_web='spam')
        self.assertFalse(Abonne.objects.exists())

    def test_retour_externe_refuse(self):
        reponse = self.inscrire('aya@example.com', depuis='https://exemple.org/')
        self.assertRedirects(reponse, '/#lettre', fetch_redirect_response=False)

    def test_reinscription_apres_desinscription(self):
        Abonne.objects.create(email='aya@example.com', actif=False)
        self.inscrire('aya@example.com')
        self.assertTrue(Abonne.objects.get(email='aya@example.com').actif)

    @override_settings(EMAIL_HOST='smtp.example.com')
    def test_email_de_bienvenue_avec_lien_de_desinscription(self):
        self.inscrire('aya@example.com')
        abonne = Abonne.objects.get()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(reverse('app:newsletter_desinscription', args=[abonne.jeton]),
                      mail.outbox[0].alternatives[0][0])

    def test_desinscription_en_deux_etapes(self):
        abonne = Abonne.objects.create(email='aya@example.com')
        url = reverse('app:newsletter_desinscription', args=[abonne.jeton])
        page = self.client.get(url)
        self.assertContains(page, 'Confirmer la désinscription')
        self.assertContains(page, 'a••••@example.com')
        abonne.refresh_from_db()
        self.assertTrue(abonne.actif)  # ouvrir le lien ne suffit pas
        page = self.client.post(url)
        self.assertContains(page, 'C&#x27;est noté.')
        abonne.refresh_from_db()
        self.assertFalse(abonne.actif)
        self.assertIsNotNone(abonne.desinscrit_le)

    def test_jeton_inconnu(self):
        reponse = self.client.get(reverse('app:newsletter_desinscription', args=['inconnu']))
        self.assertEqual(reponse.status_code, 404)

    def test_export_csv_des_abonnes_actifs(self):
        Abonne.objects.create(email='actif@example.com')
        Abonne.objects.create(email='parti@example.com', actif=False)
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'motdepasse')
        self.client.force_login(admin)
        reponse = self.client.post(reverse('admin:app_abonne_changelist'), {
            'action': 'exporter_csv',
            '_selected_action': list(Abonne.objects.values_list('pk', flat=True)),
        })
        contenu = reponse.content.decode('utf-8-sig')
        self.assertIn('actif@example.com', contenu)
        self.assertNotIn('parti@example.com', contenu)


class SecuriteTests(TestCase):
    """Réglages de production, téléversements et données structurées."""

    def reglages(self, expression, **env):
        import os
        import subprocess
        import sys
        from django.conf import settings
        code = f"from core import settings as s; print({expression})"
        environ = {k: v for k, v in os.environ.items()
                   if k not in ('SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'HSTS_SECONDS', 'ADMIN_URL')}
        environ.update(env)
        return subprocess.run([sys.executable, '-c', code], cwd=settings.BASE_DIR, env=environ,
                              capture_output=True, text=True)

    def test_production_refuses_missing_or_default_secret_key(self):
        for cle in ('', 'change-me-in-production', 'trop-courte'):
            resultat = self.reglages('s.SECRET_KEY', DEBUG='False', SECRET_KEY=cle, ALLOWED_HOSTS='uciv.org')
            self.assertNotEqual(resultat.returncode, 0, cle)
            self.assertIn('SECRET_KEY', resultat.stderr)

    def test_production_refuses_wildcard_or_empty_hosts(self):
        for hotes in ('*', ''):
            resultat = self.reglages('s.ALLOWED_HOSTS', DEBUG='False', SECRET_KEY='x' * 64, ALLOWED_HOSTS=hotes)
            self.assertNotEqual(resultat.returncode, 0, hotes)
            self.assertIn('ALLOWED_HOSTS', resultat.stderr)

    def test_production_enables_hsts_and_secure_cookies(self):
        resultat = self.reglages(
            "(s.SECURE_HSTS_SECONDS, s.SESSION_COOKIE_SECURE, s.CSRF_COOKIE_SECURE, s.SECURE_SSL_REDIRECT)",
            DEBUG='False', SECRET_KEY='x' * 64, ALLOWED_HOSTS='uciv.org', ADMIN_URL='gestion-3fa9c1d27b4e')
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        self.assertEqual(resultat.stdout.strip(), '(86400, True, True, True)')

    def test_development_keeps_working_without_variables(self):
        resultat = self.reglages('s.DEBUG', DEBUG='True')
        self.assertEqual(resultat.returncode, 0, resultat.stderr)

    def test_uploads_reject_scripts_and_oversized_files(self):
        from django.core.exceptions import ValidationError
        from django.core.files.uploadedfile import SimpleUploadedFile
        from .models import Article, Ressource
        champ_image = Article._meta.get_field('image_televersee')
        champ_fichier = Ressource._meta.get_field('fichier')
        for nom in ('piege.svg', 'page.html', 'script.js', 'image.php.txt'):
            with self.assertRaises(ValidationError, msg=nom):
                champ_image.run_validators(SimpleUploadedFile(nom, b'x'))
            with self.assertRaises(ValidationError, msg=nom):
                champ_fichier.run_validators(SimpleUploadedFile(nom, b'x'))
        champ_image.run_validators(SimpleUploadedFile('photo.webp', b'x'))
        champ_fichier.run_validators(SimpleUploadedFile('guide.pdf', b'x'))
        with self.assertRaises(ValidationError):
            champ_fichier.run_validators(SimpleUploadedFile('lourd.pdf', b'x' * (10 * 1024 * 1024 + 1)))

    def test_structured_data_cannot_break_out_of_script_tag(self):
        from .seo import _json
        texte = _json({'name': '</script><script>alert(1)</script> <!-- & fin'})
        for interdit in ('<', '>', '&'):
            self.assertNotIn(interdit, texte)
        import json
        self.assertEqual(json.loads(texte)['name'], '</script><script>alert(1)</script> <!-- & fin')


class LimiteurDeDebitTests(TestCase):
    """Au plus 5 envois par formulaire public et par adresse IP toutes les 10 minutes ; connexion à l'administration limitée."""

    FORMULAIRES = {
        'contact': ('app:contact', {'nom': 'Aya', 'email': 'aya@exemple.ci', 'objet': 'Autre', 'message': 'Bonjour'}),
        'engagement': ('app:engagement', {'nom': 'Aya', 'email': 'aya@exemple.ci', 'choix': 'volontaire'}),
        'partenaires': ('app:partenaires', {'nom': 'Awa', 'organisation': 'BonixUp', 'email': 'awa@bonixup.ci',
                                            'type_collaboration': 'Sponsoring', 'message': 'Collaborons'}),
        'newsletter': ('app:newsletter_inscription', {'email': 'lecteur@exemple.ci'}),
    }

    def envoyer(self, nom, **extra):
        nom_url, donnees = self.FORMULAIRES[nom]
        return self.client.post(reverse(nom_url), donnees, **extra)

    def test_every_public_form_is_limited_after_five_posts(self):
        for nom in self.FORMULAIRES:
            cache.clear()
            for _ in range(5):
                self.assertNotEqual(self.envoyer(nom).status_code, 429, nom)
            reponse = self.envoyer(nom)
            self.assertEqual(reponse.status_code, 429, nom)
            self.assertIn('Retry-After', reponse)
            self.assertLessEqual(int(reponse['Retry-After']), 600)

    def test_blocked_post_saves_nothing_and_page_explains(self):
        for _ in range(5):
            self.envoyer('contact')
        reponse = self.envoyer('contact')
        self.assertEqual(SoumissionContact.objects.count(), 5)
        self.assertContains(reponse, 'Erreur 429', status_code=429)
        self.assertContains(reponse, 'trop de demandes', status_code=429)
        self.assertContains(reponse, 'noindex, nofollow', status_code=429)
        self.assertContains(reponse, 'minutes', status_code=429)

    def test_reading_pages_is_never_limited(self):
        for _ in range(30):
            self.assertEqual(self.client.get(reverse('app:contact')).status_code, 200)
        self.assertNotEqual(self.envoyer('contact').status_code, 429)

    def test_forms_have_separate_counters(self):
        for _ in range(6):
            self.envoyer('contact')
        self.assertNotEqual(self.envoyer('engagement').status_code, 429)

    def test_each_address_has_its_own_counter(self):
        for _ in range(6):
            self.envoyer('contact')
        self.assertEqual(self.envoyer('contact').status_code, 429)
        self.assertNotEqual(self.envoyer('contact', REMOTE_ADDR='10.9.9.9').status_code, 429)

    @override_settings(DEBUG=False)
    def test_behind_nginx_the_real_ip_header_identifies_the_visitor(self):
        for _ in range(6):
            self.envoyer('contact', HTTP_X_REAL_IP='203.0.113.5')
        self.assertEqual(self.envoyer('contact', HTTP_X_REAL_IP='203.0.113.5').status_code, 429)
        self.assertNotEqual(self.envoyer('contact', HTTP_X_REAL_IP='203.0.113.6').status_code, 429)

    @override_settings(DEBUG=True)
    def test_in_development_the_forwarded_header_cannot_dodge_the_limit(self):
        for numero in range(5):
            self.envoyer('contact', HTTP_X_REAL_IP=f'203.0.113.{numero}')
        self.assertEqual(self.envoyer('contact', HTTP_X_REAL_IP='203.0.113.99').status_code, 429)

    def test_admin_login_is_limited_per_username_across_addresses(self):
        for numero in range(5):
            reponse = self.client.post('/back-office/login/', {'username': 'cible', 'password': 'faux'},
                                       REMOTE_ADDR=f'10.0.0.{numero}')
            self.assertEqual(reponse.status_code, 200)
        reponse = self.client.post('/back-office/login/', {'username': 'CIBLE', 'password': 'faux'}, REMOTE_ADDR='10.0.0.200')
        self.assertEqual(reponse.status_code, 429)
        self.assertIn('Retry-After', reponse)

    def test_admin_login_is_limited_per_address(self):
        for numero in range(10):
            reponse = self.client.post('/back-office/login/', {'username': f'compte{numero}', 'password': 'faux'})
            self.assertEqual(reponse.status_code, 200)
        reponse = self.client.post('/back-office/login/', {'username': 'autre', 'password': 'faux'})
        self.assertEqual(reponse.status_code, 429)

    def test_a_real_login_still_works_within_the_limit(self):
        User.objects.create_superuser('equipe', 'equipe@exemple.ci', 'mot-de-passe-solide')
        self.client.post('/back-office/login/', {'username': 'equipe', 'password': 'faux'})
        reponse = self.client.post('/back-office/login/', {'username': 'equipe', 'password': 'mot-de-passe-solide'})
        self.assertEqual(reponse.status_code, 302)

    def test_viewing_the_login_page_is_never_limited(self):
        for _ in range(20):
            self.assertEqual(self.client.get('/back-office/login/').status_code, 200)


class AdresseAdministrationTests(TestCase):
    """L'administration est à /back-office/ (réglage ADMIN_URL pour en choisir une autre) ; « admin » est refusé en production."""

    def sous_processus(self, code, **env):
        import os
        import subprocess
        import sys
        from django.conf import settings
        environ = {k: v for k, v in os.environ.items() if k not in ('SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'ADMIN_URL')}
        environ.update(env)
        return subprocess.run([sys.executable, '-c', code], cwd=settings.BASE_DIR, env=environ, capture_output=True, text=True)

    PROD = {'DEBUG': 'False', 'SECRET_KEY': 'x' * 64, 'ALLOWED_HOSTS': 'uciv.org'}
    CODE = 'from core import settings as s; print(s.ADMIN_URL)'

    def test_default_address_is_back_office_in_development_and_production(self):
        self.assertEqual(self.sous_processus(self.CODE, DEBUG='True').stdout.strip(), 'back-office')
        resultat = self.sous_processus(self.CODE, **self.PROD)
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        self.assertEqual(resultat.stdout.strip(), 'back-office')

    def test_production_refuses_admin_as_address(self):
        for valeur in ('admin', 'ADMIN', '/admin/'):
            resultat = self.sous_processus(self.CODE, **dict(self.PROD, ADMIN_URL=valeur))
            self.assertNotEqual(resultat.returncode, 0, valeur)
            self.assertIn('ADMIN_URL', resultat.stderr)

    def test_admin_url_cannot_contain_slashes_or_odd_characters(self):
        for valeur in ('gestion/secrete-123456', '../etc/passwd-123', 'gestion secrete 123'):
            resultat = self.sous_processus('from core import settings as s', **dict(self.PROD, ADMIN_URL=valeur))
            self.assertNotEqual(resultat.returncode, 0, valeur)

    def test_custom_address_moves_the_admin_and_the_default_disappears(self):
        code = ("import django; django.setup(); from django.urls import reverse, get_resolver; "
                "print(reverse('admin:index')); print([str(p.pattern) for p in get_resolver().url_patterns])")
        resultat = self.sous_processus(code, DJANGO_SETTINGS_MODULE='core.settings', **dict(self.PROD, ADMIN_URL='gestion-3fa9c1d27b4e'))
        self.assertEqual(resultat.returncode, 0, resultat.stderr)
        self.assertIn('/gestion-3fa9c1d27b4e/', resultat.stdout)
        self.assertNotIn("'back-office/'", resultat.stdout)

    def test_login_without_next_lands_on_the_admin(self):
        User.objects.create_superuser('equipe', 'equipe@exemple.ci', 'mot-de-passe-solide')
        reponse = self.client.post('/back-office/login/', {'username': 'equipe', 'password': 'mot-de-passe-solide'})
        self.assertRedirects(reponse, '/back-office/', fetch_redirect_response=False)

    def test_admin_is_served_at_back_office_and_old_address_is_gone(self):
        self.assertEqual(reverse('admin:index'), '/back-office/')
        self.assertEqual(self.client.get(reverse('admin:login')).status_code, 200)
        self.assertEqual(self.client.get('/admin/').status_code, 404)
        self.assertEqual(self.client.get('/admin/login/').status_code, 404)


class LoaderTests(TestCase):
    """Loader UCIV : écran d'attente du site public (CSS et JS dans static/, balisage dans includes/_loader.html)."""

    def html(self, nom):
        reponse = self.client.get(reverse('app:' + nom))
        self.assertEqual(reponse.status_code, 200, nom)
        return reponse.content.decode()

    def test_every_public_page_starts_with_the_loader_once(self):
        for nom in content.PAGES_INDEXABLES:
            html = self.html(nom)
            self.assertEqual(html.count('id="uciv-loader"'), 1, nom)
            self.assertLess(html.index('id="uciv-loader"'), html.index('class="skip-link"'), nom)
            self.assertGreater(html.index('id="uciv-loader"'), html.index('<body'), nom)
            self.assertIn('role="status"', html, nom)
            self.assertIn('app/assets/css/loader.css', html, nom)
            if nom == 'uciv_leadership':   # cette page a son propre loader (logo animé sur fond blanc)
                self.assertIn('app/assets/js/loader-leadership.js', html, nom)
            else:
                self.assertIn('data-once="session"', html, nom)
                self.assertIn('app/assets/js/loader.js', html, nom)
            self.assertIn('<noscript><style>#uciv-loader', html, nom)

    def test_loader_svg_ids_are_unique_and_do_not_clash_with_the_icon_sprite(self):
        import re
        html = self.html('home')
        identifiants = re.findall(r'\bid="([^"]+)"', html)
        self.assertEqual(len(identifiants), len(set(identifiants)))
        self.assertTrue(all(i.startswith(('ul-', 'uciv-loader')) or not i.startswith('ul-') for i in identifiants))

    def test_error_pages_have_the_loader_too(self):
        reponse = self.client.get('/page-qui-nexiste-pas/')
        self.assertEqual(reponse.status_code, 404)
        self.assertContains(reponse, 'id="uciv-loader"', status_code=404)

    def test_admin_does_not_show_the_loader(self):
        self.assertNotContains(self.client.get('/back-office/login/'), 'uciv-loader')

    def test_loader_files_exist_with_the_expected_api(self):
        from django.contrib.staticfiles import finders
        css = open(finders.find('app/assets/css/loader.css'), encoding='utf-8').read()
        js = open(finders.find('app/assets/js/loader.js'), encoding='utf-8').read()
        self.assertIn('prefers-reduced-motion', css)
        self.assertIn('html.uciv-loading', css)
        for api in ('UCIVLoader', 'uciv:loaded', 'replay', 'done'):
            self.assertIn(api, js)

    def test_page_animations_wait_for_the_loader(self):
        from django.contrib.staticfiles import finders
        main = open(finders.find('app/assets/js/main.js'), encoding='utf-8').read()
        self.assertIn("contains('uciv-loading')", main)
        self.assertIn("'uciv:loaded'", main)


class RejoindreLeadershipTests(TestCase):
    """Chaque « Rejoindre UCIV Leadership » ouvre le formulaire d'engagement avec l'option déjà cochée."""

    CIBLE = '/engagement/?choix=leadership#formulaire'

    def test_every_join_link_goes_to_the_form_with_the_option(self):
        import re
        total = 0
        for nom in content.PAGES_INDEXABLES:
            html = self.client.get(reverse('app:' + nom)).content.decode()
            liens = re.findall(r'<a\b[^>]*href="([^"]*)"[^>]*>\s*(?:<span>)?\s*Rejoindre UCIV Leadership', html)
            for lien in liens:
                self.assertEqual(lien, self.CIBLE, f'{nom} : {lien}')
            total += len(liens)
        self.assertGreaterEqual(total, 8)     # bandeau et menu sur 17 pages, cartes, page du programme

    def nombre(self, nom):
        return self.client.get(reverse('app:' + nom)).content.decode().count(f'href="{self.CIBLE}"')

    def test_announcement_bar_and_menu_use_the_join_link(self):
        # Sur une page neutre (contact), seuls le bandeau et le menu (ordinateur et mobile) portent le lien.
        self.assertGreaterEqual(self.nombre('contact'), 3)
        self.assertGreater(self.nombre('home'), self.nombre('contact'))      # + les cartes de l'accueil

    def test_programme_page_has_no_dead_join_button(self):
        html = self.client.get(reverse('app:uciv_leadership')).content.decode()
        self.assertEqual(self.nombre('uciv_leadership'), self.nombre('contact') + 2)   # + les deux boutons de la page
        self.assertNotIn('href="#lancement"', html)

    def test_form_opens_with_the_leadership_option_checked(self):
        html = self.client.get(reverse('app:engagement'), {'choix': 'leadership'}).content.decode()
        self.assertRegex(html, r'value="leadership"\s+checked')
        self.assertNotRegex(html, r'value="volontaire"\s+checked')

    def test_unknown_option_checks_nothing(self):
        html = self.client.get(reverse('app:engagement'), {'choix': 'nimporte-quoi'}).content.decode()
        self.assertNotRegex(html, r'name="choix" value="[a-z]+"\s+checked')

    def test_other_choices_also_land_on_the_form(self):
        html = self.client.get(reverse('app:home')).content.decode()
        self.assertIn('/engagement/?choix=volontaire#formulaire', html)
        self.assertIn('/engagement/?choix=competences#formulaire', html)

    def test_form_section_exists_as_anchor_target(self):
        html = self.client.get(reverse('app:engagement')).content.decode()
        self.assertEqual(html.count('id="formulaire"'), 1)


class MiseAJourOctobreTests(TestCase):
    """Consignes d'UCIV d'octobre 2026 (UCIV/info/uciv_update.md) et liens du site."""

    def test_leadership_programme_pages_render(self):
        for nom, titre in [('vision_action', "De la vision"), ('rh_parole', 'Les RH ont')]:
            response = self.client.get(reverse('app:' + nom))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'app/layout/programme_leadership.html')
            self.assertContains(response, titre)
            self.assertContains(response, 'Nos objectifs')
            self.assertContains(response, 'Notre conviction')
            self.assertContains(response, '/contact/?objet=Programme#ecrire')

    def test_leadership_programmes_are_linked(self):
        urls = [reverse('app:vision_action'), reverse('app:rh_parole')]
        for nom in ('uciv_leadership', 'nos_programmes', 'home'):
            html = self.client.get(reverse('app:' + nom)).content.decode()
            for url in urls:
                self.assertIn(f'href="{url}"', html, f'{url} absent de {nom}')

    def test_key_figures_are_published(self):
        self.assertEqual(Indicateur.objects.get(libelle='Jeunes mobilisés').valeur_affichee, '+1 800')
        for nom in ('home', 'impact'):
            html = self.client.get(reverse('app:' + nom)).content.decode()
            self.assertIn('+1 800', html)
            self.assertNotIn('>000<', html)
        self.assertNotContains(self.client.get(reverse('app:home')), 'Chiffres en cours de consolidation')

    def test_figure_prefix_is_optional(self):
        self.assertEqual(Indicateur(libelle='x', valeur=5).valeur_affichee, '5')
        self.assertEqual(Indicateur(libelle='x').valeur_affichee, '')

    def test_laureate_story_and_testimonial(self):
        self.assertContains(self.client.get(reverse('app:go_du_digital')), 'Leticia BOSSON')
        self.assertContains(self.client.get(reverse('app:impact')), 'Leticia BOSSON, Reine du Digital')
        histoire = Article.objects.get(slug='histoire-la-laureate-de-la-reine-du-digital')
        self.assertTrue(histoire.chapo.startswith('Leticia BOSSON'))
        self.assertNotIn('[Nom de la lauréate]', histoire.chapo)
        self.assertEqual(histoire.image, 'app/assets/img/leticia-bosson.webp')
        actualite = Article.objects.get(slug='la-reine-du-digital-le-parcours-d-une-laureate')
        self.assertEqual(actualite.image, 'app/assets/img/leticia-bosson.webp')
        self.assertIn('Leticia BOSSON', actualite.titre)
        self.assertTrue(actualite.chapo.startswith('Leticia BOSSON'))
        reponse = self.client.get(reverse('app:actualites'))
        self.assertContains(reponse, 'Leticia BOSSON')
        self.assertContains(reponse, 'leticia-bosson.webp')
        self.assertContains(self.client.get(actualite.get_absolute_url()), 'Leticia BOSSON')

    def test_empty_testimonials_are_hidden(self):
        self.assertNotContains(self.client.get(reverse('app:experience_lab')), 'id="temoignages"')

    def test_team_page_shows_every_member_with_photo(self):
        html = self.client.get(reverse('app:equipe')).content.decode()
        for groupe in content.EQUIPE['groupes']:
            for membre in groupe['membres']:
                self.assertIn(membre['nom'], html)
                self.assertIn(membre['photo'].split('/')[-1], html)
        self.assertNotIn('[Courte biographie', html)

    def test_hero_shapes_replace_circles(self):
        for nom in ('home', 'go_du_digital', 'vision_action', 'impact', 'equipe'):
            html = self.client.get(reverse('app:' + nom)).content.decode()
            self.assertIn('class="forme-uciv"', html, nom)
        self.assertNotIn('hero__disque', self.client.get(reverse('app:home')).content.decode())

    def test_search(self):
        response = self.client.get(reverse('app:recherche'), {'q': 'leadership'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('app:vision_action'))
        self.assertContains(self.client.get(reverse('app:recherche'), {'q': 'ressources humaines'}),
                            reverse('app:rh_parole'))
        self.assertContains(self.client.get(reverse('app:recherche'), {'q': 'zzzzzz'}), 'Aucun résultat')
        self.assertEqual(self.client.get(reverse('app:recherche')).status_code, 200)
        self.assertEqual(self.client.get(reverse('app:recherche'), {'q': '<script>' * 50}).status_code, 200)

    def test_search_is_not_indexed(self):
        self.assertContains(self.client.get(reverse('app:recherche'), {'q': 'go'}), 'noindex')

    def test_no_dead_links(self):
        """Aucun lien « # » vide, et chaque lien interne des pages du site répond (200 ou redirection)."""
        import re
        pages = [reverse('app:' + nom) for nom in content.PAGES_INDEXABLES]
        pages += [reverse('app:recherche'), reverse('app:mentions_legales'), reverse('app:confidentialite'),
                  reverse('app:conditions')]
        pages += [a.get_absolute_url() for a in Article.objects.filter(publish=True)[:3]]
        vus = set()
        for page in pages:
            html = self.client.get(page).content.decode()
            self.assertNotIn('href="#"', html, page)
            for lien in re.findall(r'href="(/[^"#]*)', html):
                if lien in vus or lien.startswith(('/static/', '/media/')):
                    continue
                vus.add(lien)
                statut = self.client.get(lien).status_code
                self.assertIn(statut, (200, 301, 302), f'{lien} (depuis {page}) : {statut}')
        self.assertGreater(len(vus), 30)


class CadrageImagesTests(TestCase):
    """Les images d'articles sont recadrées sur les visages (champ image_position)."""

    def test_photos_existantes_sont_cadrees(self):
        cadrages = dict(Article.objects.values_list('image', 'image_position'))
        self.assertEqual(cadrages['app/assets/img/partenariat-paipro.webp'], 'center 10%')
        self.assertNotEqual(cadrages['app/assets/img/volontaires-terrain.webp'], 'center')

    def test_cadrage_applique_aux_cartes_et_a_l_article(self):
        article = Article.objects.get(image='app/assets/img/partenariat-paipro.webp')
        self.assertContains(self.client.get(reverse('app:actualites')), 'object-position: center 10%')
        self.assertContains(self.client.get(article.get_absolute_url()), 'object-position: center 10%')
        self.assertContains(self.client.get(reverse('app:home')), 'object-position: center 10%')

    def test_cadrage_invalide_refuse(self):
        from django.core.exceptions import ValidationError
        from .validators import valider_position_image
        for valeur in ('center', 'center 20%', '60% center', 'top'):
            valider_position_image(valeur)
        for valeur in ('center; background:red', 'url(x)', '20px 10px', ''):
            with self.assertRaises(ValidationError):
                valider_position_image(valeur)


class BoutonsHeroAccueilTests(TestCase):
    """Les deux boutons du bandeau d'accueil mènent à des pages, pas à une ancre de la page."""

    def test_boutons_du_bandeau(self):
        html = self.client.get(reverse('app:home')).content.decode()
        bandeau = html[html.index('hero__cta'):html.index('hero__parcours')]
        self.assertIn(f'href="{reverse("app:engagement")}"', bandeau)
        self.assertIn("Je veux m'engager", bandeau)
        self.assertIn(f'href="{reverse("app:qui_sommes_nous")}"', bandeau)
        self.assertNotRegex(bandeau, r'<a [^>]*href="#')

    def test_le_decor_du_bandeau_ne_recouvre_pas_les_boutons(self):
        """Sur grand écran le bloc de la photo s'étend sur tout le bandeau : il doit laisser passer les clics."""
        from pathlib import Path
        from django.conf import settings
        css = (Path(settings.BASE_DIR) / 'static' / 'app' / 'assets' / 'css' / 'main.css').read_text(encoding='utf-8')
        bloc = css[css.index('.hero__visuel {' + chr(10) + '    --k: 1'):]
        bloc = bloc[:bloc.index('}')]
        self.assertIn('pointer-events: none', bloc)
        self.assertIn('.hero__texte { position: absolute; z-index: 2;', css)


class BoutonProgrammesLeadershipTests(TestCase):
    def test_decouvrir_nos_programmes_mene_a_la_section_du_reseau(self):
        html = self.client.get(reverse('app:uciv_leadership')).content.decode()
        self.assertIn('href="#programmes-du-reseau">Découvrir nos programmes</a>', html)
        self.assertIn('id="programmes-du-reseau"', html)


class CarteLeadershipAccueilTests(TestCase):
    def test_la_carte_leadership_utilise_la_photo_de_couverture(self):
        html = self.client.get(reverse('app:home')).content.decode()
        carte = html[html.index('programmes__cartes'):]
        self.assertIn('leadership-couverture.webp', carte)
        self.assertNotIn('groupe-nb.webp', carte[:carte.index('</ul>')])


class FormeLogoSectionsTests(TestCase):
    """Les anneaux décoratifs des sections prennent la forme du logo (comme les bandeaux)."""

    def test_les_anneaux_des_sections_utilisent_le_masque_du_logo(self):
        from pathlib import Path
        from django.conf import settings
        statique = Path(settings.BASE_DIR) / 'static' / 'app' / 'assets'
        css = (statique / 'css' / 'main.css').read_text(encoding='utf-8')
        bloc = css[css.index('/* 29. Forme du logo dans les sections'):]
        for classe in ('vision__anneau', 'lead-pourquoi__anneau', 'np-appel__anneau', 'gd-inscriptions__disque',
                       'imp-carte__anneau', 'con-coord__anneau', 'leg-question__anneau'):
            self.assertIn('.' + classe, bloc, classe)
        self.assertIn('mask: url("../img/forme-uciv.svg")', bloc)
        self.assertIn('.qs-vision::before, .qs-citation::before', bloc)
        self.assertIn('.eng-hero::before', bloc)
        self.assertTrue((statique / 'img' / 'forme-uciv.svg').exists())


class StatiqueAvecEmpreinteTests(TestCase):
    """Le navigateur garde les statiques 30 jours : l'adresse doit changer quand le fichier change."""

    def test_pages_chargent_le_css_avec_empreinte(self):
        import re
        html = self.client.get(reverse('app:home')).content.decode()
        self.assertRegex(html, r'/static/app/assets/css/main\.css\?v=[0-9a-f]{10}"')
        self.assertRegex(html, r'/static/app/assets/js/main\.js\?v=[0-9a-f]{10}"')

    def test_empreinte_suit_le_contenu(self):
        import tempfile
        from pathlib import Path
        from core.storage import StatiqueAvecEmpreinte
        with tempfile.TemporaryDirectory() as dossier:
            stockage = StatiqueAvecEmpreinte(location=dossier, base_url='/static/')
            fichier = Path(dossier) / 'a.css'
            fichier.write_text('a{color:red}', encoding='utf-8')
            avant = stockage.url('a.css')
            self.assertEqual(avant, stockage.url('a.css'))
            fichier.write_text('a{color:blue}', encoding='utf-8')
            self.assertNotEqual(avant, stockage.url('a.css'))
            self.assertEqual(stockage.url('absent.css'), '/static/absent.css')


class BandeauPartenairesTests(TestCase):
    def test_photo_du_bandeau_cadree_sur_les_visages(self):
        """La photo est un portrait dont les visages sont en haut : le recadrage ne doit pas viser le centre."""
        from pathlib import Path
        from django.conf import settings
        css = (Path(settings.BASE_DIR) / 'static' / 'app' / 'assets' / 'css' / 'main.css').read_text(encoding='utf-8')
        regle = css[css.index('.par-hero__photo img {'):]
        regle = regle[:regle.index('}')]
        self.assertIn('object-position: center top', regle)
        self.assertContains(self.client.get(reverse('app:partenaires')), 'par-hero__photo')


class LoaderLeadershipTests(TestCase):
    """La page UCIV Leadership a son loader (logo animé sur fond blanc) à la place de celui du site."""

    def test_page_leadership_utilise_son_loader(self):
        html = self.client.get(reverse('app:uciv_leadership')).content.decode()
        self.assertIn('uciv-loader--leadership', html)
        self.assertIn('loader-leadership.js', html)
        self.assertIn('logo-uciv-leadership.webp', html)
        self.assertIn('uciv-loader__panel', html)
        self.assertNotIn('uciv-loader__accent', html)   # pas de rideau orange : on découvre directement le jaune du bandeau
        self.assertNotIn('app/assets/js/loader.js', html)

    def test_les_autres_pages_gardent_le_loader_du_site(self):
        for nom in ('home', 'qui_sommes_nous', 'partenaires'):
            html = self.client.get(reverse('app:' + nom)).content.decode()
            self.assertIn('uciv-loader__panel', html, nom)
            self.assertNotIn('uciv-loader--leadership', html, nom)

    def test_adresse_de_leadership_exposee_pour_le_voile(self):
        html = self.client.get(reverse('app:home')).content.decode()
        self.assertIn(f'data-url-leadership="{reverse("app:uciv_leadership")}"', html)

    def test_fichiers_du_loader_existent(self):
        from pathlib import Path
        from django.conf import settings
        statique = Path(settings.BASE_DIR) / 'static' / 'app' / 'assets'
        self.assertTrue((statique / 'js' / 'loader-leadership.js').exists())
        self.assertTrue((statique / 'img' / 'logo-uciv-leadership.webp').exists())
        css = (statique / 'css' / 'loader.css').read_text(encoding='utf-8')
        self.assertIn('.uciv-loader--leadership', css)
        self.assertIn('.uciv-loader--leadership .uciv-loader__panel{background:#fff}', css)
        # mobile : vert profond du site ; ordinateur : logo réduit
        self.assertIn('@media (max-width:719px){.uciv-loader--leadership .uciv-loader__panel{background:#0c3322}}', css)
        self.assertIn('@media (min-width:720px){.uciv-loader--leadership .ull{width:min(72vw,680px)}}', css)
        # sortie : le panneau monte (mêmes règles que le loader du site) ; le loader Leadership n'a pas de rideau orange
        self.assertIn('.uciv-loader.is-leaving .uciv-loader__panel{animation:ul-curtain', css)


class FormesPagesErreurEtTabletteTests(TestCase):
    """Anneaux des pages d'erreur remplacés par la forme du logo ; bandeau Partenaires lisible en tablette."""

    def css(self):
        from pathlib import Path
        from django.conf import settings
        return (Path(settings.BASE_DIR) / 'static' / 'app' / 'assets' / 'css' / 'main.css').read_text(encoding='utf-8')

    def test_anneaux_des_pages_d_erreur_prennent_la_forme_du_logo(self):
        bloc = self.css()
        bloc = bloc[bloc.index('/* 30. Pages d'+"'"+'erreur'):]
        bloc = bloc[:bloc.index('}')]
        self.assertIn('.err__anneau, .err__jaune', bloc)
        self.assertIn('mask: url("../img/forme-uciv.svg")', bloc)
        # plus de dégradé en anneau sur ces deux éléments
        css = self.css()
        for regle in ('.err__anneau {', '.err__jaune {'):
            ligne = css[css.index(regle):].split(chr(10))[0]
            self.assertNotIn('radial-gradient', ligne, regle)

    def test_pages_d_erreur_s_affichent(self):
        reponse = self.client.get('/page-qui-n-existe-pas/')
        self.assertEqual(reponse.status_code, 404)
        self.assertContains(reponse, 'err__anneau', status_code=404)
        self.assertContains(reponse, 'err__jaune', status_code=404)

    def test_bandeau_partenaires_utilise_la_forme_translucide_en_tablette(self):
        css = self.css()
        bloc = css[css.index('/* 31. Bandeau Partenaires en tablette'):]
        self.assertIn('@media (min-width: 720px) and (max-width: 899px)', bloc)
        self.assertIn('.par-hero .formes-uciv--desktop { display: none; }', bloc)
        self.assertIn('.par-hero .formes-uciv--mobile', bloc)


class ConfigurationEmailTests(TestCase):
    """Envoi d'e-mails : expéditeur, commande de test et script de configuration du serveur."""

    def test_expediteur_est_default_from_email(self):
        from core.utils import send_customize_email
        with override_settings(DEFAULT_FROM_EMAIL='equipe@exemple.ci'):
            self.assertTrue(send_customize_email("Sujet", ['dest@exemple.ci'], 'emails/newsletter_bienvenue.html',
                                                 {'lien_desinscription': 'https://exemple.ci/x/'}))
        self.assertEqual(mail.outbox[0].from_email, 'equipe@exemple.ci')

    def test_delai_smtp_borne(self):
        from django.conf import settings
        self.assertGreater(settings.EMAIL_TIMEOUT, 0)   # sans délai, un SMTP muet bloquerait un worker
        self.assertFalse(settings.EMAIL_USE_SSL and settings.EMAIL_USE_TLS)

    @override_settings(EMAIL_HOST='smtp.exemple.test', EMAIL_HOST_USER='envoi@exemple.ci',
                       EMAIL_HOST_PASSWORD='secret-a-ne-jamais-afficher', DEFAULT_FROM_EMAIL='envoi@exemple.ci')
    def test_commande_tester_email_envoie_et_ne_montre_pas_le_mot_de_passe(self):
        from io import StringIO
        from django.core.management import call_command
        sortie = StringIO()
        call_command('tester_email', 'test@exemple.ci', stdout=sortie)
        self.assertEqual(mail.outbox[0].to, ['test@exemple.ci'])
        self.assertEqual(mail.outbox[0].from_email, 'envoi@exemple.ci')
        texte = sortie.getvalue()
        self.assertIn('smtp.exemple.test', texte)
        self.assertNotIn('secret-a-ne-jamais-afficher', texte)

    @override_settings(EMAIL_HOST='', CONTACT_EMAIL='equipe@exemple.ci')
    def test_commande_tester_email_refuse_sans_serveur(self):
        from django.core.management import call_command
        from django.core.management.base import CommandError
        with self.assertRaisesMessage(CommandError, 'EMAIL_HOST est vide'):
            call_command('tester_email')
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_HOST='smtp.exemple.test')
    def test_commande_tester_email_remonte_l_erreur_du_serveur(self):
        import smtplib
        from unittest import mock
        from django.core.management import call_command
        from django.core.management.base import CommandError
        erreur = smtplib.SMTPAuthenticationError(535, b'Username and Password not accepted')
        with mock.patch('app.management.commands.tester_email.send_mail', side_effect=erreur):
            with self.assertRaisesMessage(CommandError, 'SMTPAuthenticationError'):
                call_command('tester_email', 'test@exemple.ci')

    def test_script_de_configuration_ne_contient_aucun_secret(self):
        from pathlib import Path
        from django.conf import settings
        script = Path(settings.BASE_DIR).parent / 'deploy' / 'configurer_email.sh'
        texte = script.read_text(encoding='utf-8')
        self.assertIn('read -r -s', texte)               # mot de passe saisi sans affichage
        self.assertIn('uciv-manage tester_email', texte)
        self.assertIn('chmod 600', texte)
        self.assertIn('smtp.hostinger.com', texte)        # adresse professionnelle du domaine (Hostinger)
        self.assertIn('smtp-relay.brevo.com', texte)      # service d'envoi avec expéditeur @uciv.org, sans boîte mail
        # chaque option annoncée par le menu (1 à 4) a son bloc de saisie, et il y a un seul serveur par option
        for choix, serveur in (('1', 'smtp-relay.brevo.com'), ('2', 'smtp.hostinger.com'), ('3', 'smtp.gmail.com')):
            self.assertIn('elif [ "${CHOIX}" = "%s" ]' % choix if choix != '1' else 'if [ "${CHOIX}" = "1" ]', texte)
            self.assertIn('HOTE=%s;' % serveur, texte)
        self.assertIn('elif [ "${CHOIX}" = "4" ]', texte)
        self.assertIn('CONTACT_EMAIL', texte)
        self.assertNotRegex(texte, r'EMAIL_HOST_PASSWORD=[^%\s]')   # jamais de valeur écrite en dur

    def test_bienvenue_newsletter_repond_a_l_equipe(self):
        """L'adresse d'envoi n'a pas de boîte : une réponse au message de bienvenue doit aller à CONTACT_EMAIL."""
        with override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.ci',
                               DEFAULT_FROM_EMAIL='contact@exemple.ci'):
            self.client.post(reverse('app:newsletter_inscription'), {'email': 'nouveau@exemple.ci'})
        bienvenue = [m for m in mail.outbox if m.to == ['nouveau@exemple.ci']]
        self.assertEqual(len(bienvenue), 1)
        self.assertEqual(bienvenue[0].from_email, 'contact@exemple.ci')
        self.assertEqual(bienvenue[0].reply_to, ['equipe@exemple.ci'])

    @override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.ci',
                       DEFAULT_FROM_EMAIL='UCIV <noreply@exemple.ci>')
    def test_accuse_envoye_depuis_noreply_une_seule_fois_par_heure_et_par_adresse(self):
        donnees = {'nom': 'Awa Traoré', 'email': 'Awa@Exemple.ci', 'telephone': '', 'organisation': '',
                   'objet': 'Presse-média', 'message': 'Première question.'}
        self.client.post(reverse('app:contact'), donnees)
        self.client.post(reverse('app:contact'), {**donnees, 'email': 'awa@exemple.ci', 'message': 'Seconde question.'})
        # deux notifications à l'équipe, mais un seul accusé pour la même adresse (casse ignorée)
        self.assertEqual(len([m for m in mail.outbox if m.to == ['equipe@exemple.ci']]), 2)
        accuses = [m for m in mail.outbox if m.to != ['equipe@exemple.ci']]
        self.assertEqual(len(accuses), 1)
        self.assertEqual(accuses[0].from_email, 'UCIV <noreply@exemple.ci>')

    @override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.ci')
    def test_echec_de_l_accuse_ne_bloque_pas_la_prochaine_tentative(self):
        from unittest import mock
        from core import utils
        with mock.patch.object(utils, 'send_customize_email', return_value=False):
            self.assertFalse(utils.envoyer_accuse_reception('x@exemple.ci', 'Sujet', 'emails/accuse_reception.html', {}))
        with mock.patch.object(utils, 'send_customize_email', return_value=True):
            self.assertTrue(utils.envoyer_accuse_reception('x@exemple.ci', 'Sujet', 'emails/accuse_reception.html', {}))


class StyleDesEmailsTests(TestCase):
    """Cadre commun des e-mails : charte UCIV, adresse de l'équipe visible, version texte brut."""

    GABARITS = {
        'emails/contact.html': {'soumission': {'nom': 'Awa', 'email': 'awa@exemple.ci', 'telephone': '', 'organisation': '',
                                               'objet': 'Autre', 'message': 'Bonjour.'}},
        'emails/engagement.html': {'soumission': {'nom': 'Aya', 'email': 'aya@exemple.ci', 'telephone': '', 'competences': '',
                                                  'message': 'Disponible.'}},
        'emails/partenariat.html': {'soumission': {'nom': 'Yao', 'organisation': 'Test', 'email': 'yao@exemple.ci', 'telephone': '',
                                                   'type_collaboration': 'Sponsoring', 'message': 'Soutien.'}},
        'emails/accuse_reception.html': {'soumission': {'nom': 'Awa', 'message': 'Bonjour.'}, 'demande': 'votre message'},
        'emails/newsletter_bienvenue.html': {'lien_desinscription': 'https://uciv.org/newsletter/desinscription/abc123/'},
    }

    @override_settings(CONTACT_EMAIL='organisationuciv@gmail.com', SITE_URL='https://uciv.org')
    def test_chaque_email_affiche_l_adresse_de_l_equipe_et_la_charte(self):
        from django.template.loader import render_to_string
        from core.utils import contexte_email
        for gabarit, ctx in self.GABARITS.items():
            html = render_to_string(gabarit, contexte_email(ctx))
            self.assertIn('href="mailto:organisationuciv@gmail.com"', html, gabarit)
            self.assertIn('Écrire directement à l\'équipe', html, gabarit)
            self.assertIn('https://uciv.org/static/app/assets/img/logo-uciv.png', html, gabarit)   # logo en adresse absolue
            for couleur in ('#E17F1C', '#0C3322', '#FBF5EA'):
                self.assertIn(couleur, html, f'{gabarit} {couleur}')

    @override_settings(EMAIL_HOST='smtp.exemple.test', CONTACT_EMAIL='equipe@exemple.ci')
    def test_les_messages_ont_une_version_texte_brut(self):
        from core.utils import send_customize_email
        self.assertTrue(send_customize_email('Sujet', ['dest@exemple.ci'], 'emails/newsletter_bienvenue.html',
                                             {'lien_desinscription': 'https://uciv.org/newsletter/desinscription/abc123/'}))
        message = mail.outbox[0]
        self.assertNotIn('<', message.body)                                   # pas de balises
        self.assertIn('equipe@exemple.ci', message.body)                      # l'adresse de l'équipe figure aussi en texte
        self.assertIn('https://uciv.org/newsletter/desinscription/abc123/', message.body)   # lien de désinscription lisible
        self.assertNotIn('display:none', message.body)                        # texte d'aperçu masqué non recopié

    def test_texte_brut_remplace_les_liens_par_texte_et_adresse(self):
        from core.utils import texte_brut
        texte = texte_brut('<p>Lisez <a href="https://uciv.org/actualites/">nos actualités</a> ou écrivez à '
                           '<a href="mailto:a@b.ci">a@b.ci</a>.</p><a href="https://uciv.org"><img src="x.png" alt=""></a>')
        self.assertEqual(texte, 'Lisez nos actualités (https://uciv.org/actualites/) ou écrivez à a@b.ci.')
