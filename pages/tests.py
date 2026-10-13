from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_home_renders(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_home_shows_key_content(self):
        response = self.client.get(reverse('pages:home'))
        self.assertContains(response, "Une Côte d'Ivoire")
        self.assertContains(response, 'Les Go du Digital')
        self.assertContains(response, 'UCIV Leadership')
        self.assertContains(response, 'Experience Lab')
        self.assertContains(response, 'organisationuciv@gmail.com')
