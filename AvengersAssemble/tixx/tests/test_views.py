from django.test import TestCase
from django.urls import reverse
from tixx.models import Event 
from django.test import Client

# Sample test for the events tab.

class EventsViewTest(TestCase):
    def test_eventsView(self):
        Event.objects.create(title='Event 1', date='2024-03-05')
        Event.objects.create(title='Event 2', date='2024-03-06')

        response = self.client.get(reverse('events'))

        self.assertEqual(response.status_code, 200)
        expected = ['Event 1', 'Event 2']
        actual = [event.title for event in response.context['events']]

        self.assertListEqual(actual, expected)
        
