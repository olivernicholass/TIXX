from django.test import TestCase, RequestFactory
from django.urls import reverse
from tixx.models import Event

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
                
    # Browser Test for Figure
    def test_figure(self):
        figure_name = "Test Figure"
        url = reverse('figure', kwargs={'figure_name': figure_name})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
# Filtered Events Test 

class FilteredEventsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.event1 = Event.objects.create(
            eventName="Event 1",
            eventDate="2024-03-10",
            eventId=1,
            eventLocation="Location 1",
            eventDescription="Description 1",
            eventStatus="Upcoming",
            eventGenre="Genre-1"
        )
        self.event2 = Event.objects.create(
            eventName="Event 2",
            eventDate="2024-03-11",
            eventId=2,
            eventLocation="Location 2",
            eventDescription="Description 2",
            eventStatus="Upcoming",
            eventGenre="Genre-2"
        )

    def test_filtered_events_view(self):
        url = reverse('filtered_events', kwargs={'eventGenre': 'Genre-1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filtered_events.html')
        filtered_events = response.context['filtered_events']
        self.assertEqual(len(filtered_events), 1)
        self.assertEqual(filtered_events[0], self.event1)
