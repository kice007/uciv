from django.test import TestCase
from django.urls import reverse


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
