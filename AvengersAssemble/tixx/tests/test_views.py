from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from tixx.models import Figure, Event, Review, ReviewImage, Arena
from django.utils.text import slugify

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
    
# Filtered Events Test 

class FilteredEventsTestCase(TestCase):
    def setUp(self):
        self.arena = Arena.objects.create(arenaId='A001', arenaName='Test Arena', arenaCapacity=1000)
        self.figure = Figure.objects.create(figureName='Test Figure', figureGenre='Genre-1')
        self.event1 = Event.objects.create(
            eventName="Event 1",
            eventDate=timezone.now().date(),
            eventTime=timezone.now().time(),
            eventId=1,
            eventLocation="Location 1",
            eventDescription="Description 1",
            eventStatus="Upcoming",
            eventGenre="Genre-1",
            arenaId=self.arena,
            figureId=self.figure
        )

    def test_filtered_events_view(self):
        url = reverse('filtered_events', kwargs={'eventGenre': 'Genre-1'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'filtered_events.html')
        filtered_events = response.context['filtered_events']
        self.assertEqual(len(filtered_events), 1) 
        self.assertEqual(filtered_events[0], self.event1)

# Figure View Test

class FigureViewTestCase(TestCase):
    def setUp(self):
        self.figure = Figure.objects.create(
            figureName="Test Figure",
            figureGenre="Test Genre"
        )

        self.reviewNoImage = Review.objects.create(
            reviewRating=4,
            reviewTitle="Test Review Without Image",
            reviewText="Test Review Text Without Image",
            reviewFigure=self.figure,
            reviewDate="2024-03-19"
        )

        self.reviewWithImage = Review.objects.create(
            reviewRating=4,
            reviewTitle="Test Review With Image",
            reviewText="Test Review Text With Image",
            reviewFigure=self.figure,
            reviewDate="2024-03-19"
        )
        
        self.review_image = ReviewImage.objects.create(
            review=self.reviewWithImage,
            reviewImage="review_images/test_image.jpg"
        )

        self.event = Event.objects.create(
            eventName="Test Event",
            eventDate="2024-03-19",
            eventTime="12:00",
            eventLocation="Test Location",
            eventDescription="Test Description",
            eventStatus="Test Status",
            figureId=self.figure  
        )

    def test_figure_view(self):
        url = reverse('figure', args=[self.figure.figureName])
        response = self.client.get(url)
        
       # Page Response
        self.assertEqual(response.status_code, 200)

        # Figure is passed to template
        self.assertEqual(response.context['figure'], self.figure)

        # Reviews related to figure are passed to template (w/ Images and w/ out Images)
        self.assertIn(self.reviewWithImage, response.context['allReviews'])
        self.assertIn(self.reviewNoImage, response.context['allReviews'])

        # Accurate review count
        self.assertEqual(response.context['reviewCount'], 2) 

        # Correct Template
        self.assertTemplateUsed(response, 'figure.html')