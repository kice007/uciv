from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import SoumissionContact, SoumissionEngagement, SoumissionPartenariat


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
