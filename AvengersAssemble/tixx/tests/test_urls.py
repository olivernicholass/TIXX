from django.test import TestCase
from django.urls import reverse

class UrlTestCase(TestCase):
    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_search_results_url(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_selection_url(self):
        response = self.client.get(reverse('ticket_selection', args=['1']))
        self.assertEqual(response.status_code, 404)

    def test_checkout_url(self):
        selected_seats = 'A1,C2,B5'  # Replace 'your_selected_seats_here' with actual seat selection
        response = self.client.get(reverse('checkout', args=[selected_seats]))
        self.assertEqual(response.status_code, 200)

    def test_filtered_events_url(self):
        response = self.client.get(reverse('filtered_events', args=['some_genre']))
        self.assertEqual(response.status_code, 200)

    def test_figure_url(self):
        response = self.client.get(reverse('figure', args=['some_figure']))
        self.assertEqual(response.status_code, 404)
