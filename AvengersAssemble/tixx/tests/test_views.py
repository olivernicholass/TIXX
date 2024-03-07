from django.test import TestCase
from django.urls import reverse

class ViewTests(TestCase):
    
    # Browser Test for Home
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # Browser Test for Login
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        
    # Browser Test for Profile
    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    # Browser Test for Register
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    # Browser Test for Search Results
    def test_search_results_view(self):
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_results.html')

    # Browser Test for Ticket Selection
    def test_ticket_selection_view(self):
        response = self.client.get(reverse('ticket_selection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ticket_selection.html')

    # Browser Test for Checkout
    def test_checkout_view(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')

    # Browser Test for Filtered Events
    def test_filtered_events_view(self):
        response = self.client.get(reverse('filtered_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filtered_events.html')
