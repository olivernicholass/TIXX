from django.test import TestCase
from django.test import Client, TestCase
from django.urls import reverse
from tixx.models import User

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

    def test_search_results_url(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)

    def test_ticket_selection_url(self):
        response = self.client.get(reverse('ticket_selection', args=['1']))
        self.assertEqual(response.status_code, 404)

    def test_checkout_url(self):
        event_id = 1
        selected_seats = 'S1A1,S1B2,S1C3'  # Replace 'your_selected_seats_here' with actual seat selection
        response = self.client.get(reverse('checkout', args=[event_id, selected_seats]))
        self.assertEqual(response.status_code, 200)

    def test_filtered_events_url(self):
        response = self.client.get(reverse('filtered_events', args=['some_genre']))
        self.assertEqual(response.status_code, 200)

    def test_figure_url(self):
        response = self.client.get(reverse('figure', args=['some_figure']))
        self.assertEqual(response.status_code, 404)

    def test_checkout_url(self):
        response = self.client.get(reverse('figure', args=['some_checkout']))
        self.assertEqual(response.status_code, 404)

