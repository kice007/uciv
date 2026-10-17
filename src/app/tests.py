from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from . import content
from .models import (
    Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)


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
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['equipe@exemple.test'])
        self.assertIn('Aya Konan', mail.outbox[0].alternatives[0][0])

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
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['equipe@exemple.test'])

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
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].reply_to, ['awa@exemple.ci'])

    def test_footer_links_to_page(self):
        response = self.client.get(reverse('app:home'))
        self.assertContains(response, reverse('app:contact'))

class ContenuModelsTests(TestCase):
    def test_article_image_url_prefers_static_path(self):
        article = Article.objects.create(
            titre='Un article', slug='un-article', categorie='activites',
            date_publication='2026-10-01', image='app/assets/img/groupe-nb.png',
        )
        self.assertTrue(article.image_url.endswith('app/assets/img/groupe-nb.png'))
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
    def test_login_page_wears_uciv_branding(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'app/assets/css/admin.css')
        self.assertContains(response, 'uciv-marque')
        self.assertContains(response, 'Administration UCIV')

    def test_dashboard_shows_site_models(self):
        from django.contrib.auth import get_user_model
        get_user_model().objects.create_superuser('equipe', 'equipe@exemple.ci', 'mot-de-passe-solide')
        self.client.login(username='equipe', password='mot-de-passe-solide')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Site UCIV')
        self.assertContains(response, 'Gestion du site')
        self.assertContains(response, 'Articles')
        self.assertContains(response, 'Opportunités')
        self.assertEqual(self.client.get('/admin/app/article/').status_code, 200)


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
        self.assertIn('Disallow: /admin/', texte)
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
        self.assertIn('Page <em>introuvable.</em>', html)
