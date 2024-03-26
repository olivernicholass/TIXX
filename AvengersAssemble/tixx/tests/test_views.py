from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from tixx.models import Figure, Event, Review, ReviewImage, Arena
from django.utils.text import slugify
from django.test import TestCase
from tixx.views import review
from tixx.forms import ReviewForm, ReviewImageForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import datetime

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
    class TicketSelectionTestCase(TestCase):
        def setup(self):
            self.event = Event.objects.create(            
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
        # Browser Test for Ticket Selection
        def test_ticket_selection_view(self):
            response = self.client.get(reverse('ticket_selection',  kwargs={'eventGenre': 'Genre-1'}))
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

# Review View Test (100% Coverage)

class ReviewViewTest(TestCase):
    def setUp(self):
        
        # Sample figure 
        self.figure = Figure.objects.create(
            figureName='Test Figure',
            figureGenre='Test Genre',
            figureAbout='Test About'
        )

        # Sample review 
        self.review = Review.objects.create(
            reviewRating=4.5,
            reviewTitle='Test Review',
            reviewText='Test Review Text',
            reviewFigure=self.figure,
            reviewDate=datetime.date.today()
        )

        self.client = Client()

    # Handling a GET request PRE submission
    
    def test_review_view_get(self):
        url = reverse('review', kwargs={'figure_name': self.figure.figureName})
        response = self.client.get(url)
        
        # Asserting various responses on context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')
        self.assertIn('reviewForm', response.context)
        self.assertIn('imageForm', response.context)
        self.assertIn('figure', response.context)
        self.assertIn('averageRating', response.context)
        self.assertIn('formValidity', response.context)
        self.assertEqual(response.context['figure'], self.figure)
        self.assertEqual(response.context['averageRating'], 4.5)
        self.assertFalse(response.context['formValidity'])

    # Handling a POST request after submitting a review
    
    def test_review_view_post(self):
        url = reverse('review', kwargs={'figure_name': self.figure.figureName})
        response = self.client.post(url, {
            'reviewRating': 4.0,
            'reviewTitle': 'Test Review',
            'reviewText': 'Test Review Text',
            'reviewDate': datetime.date.today()
        }, format='multipart')  
        
        # Asserting various responses on context
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')
        self.assertIn('reviewForm', response.context)
        self.assertIn('imageForm', response.context)
        self.assertIn('figure', response.context)
        self.assertIn('averageRating', response.context)
        self.assertIn('formValidity', response.context)
        self.assertEqual(response.context['figure'], self.figure)
        self.assertIsNotNone(response.context['averageRating'])
        self.assertTrue(response.context['formValidity'])
        
# Search Results View Test (0.967 -> 97% Coverage)

class SearchResultsViewTest(TestCase):
    
    # SET UP LOCAL IMAGE UPLOAD
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testJPG= cls.testImage()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @staticmethod
    def testImage():
        return SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")

    def setUp(self):
        # TEST FIGURES
        self.figure1 = Figure.objects.create(figureName='Drake', figureGenre='Hip-Hop', figurePicture=self.testJPG)
        self.figure2 = Figure.objects.create(figureName='Adele', figureGenre='Pop', figurePicture=self.testJPG)

        # TEST EVENTS/ARENA
        self.arena = Arena.objects.create(arenaId='12345', arenaName='Test Arena', arenaCapacity=10000)
        self.event1 = Event.objects.create(eventName='Drake Concert', eventDate='2024-05-30', eventTime='20:00',
                                            eventLocation='Vancouver', eventDescription='Concert', eventStatus='Active',
                                            arenaId=self.arena, figureId=self.figure1)
        self.event2 = Event.objects.create(eventName='Adele Concert', eventDate='2024-05-30', eventTime='19:00',
                                            eventLocation='Vancouver', eventDescription='Concert', eventStatus='Active',
                                            arenaId=self.arena, figureId=self.figure2)
        super().setUp()

    # TAKE DOWN IMAGES
    def tearDown(self):
        super().tearDown()
        self.figure1.figurePicture.delete()
        self.figure2.figurePicture.delete()

    # TEST: Handle City + Date + Keyword 
    def test_search_results_exact_city_date_query(self):

        Query = {
            'searchQuery': 'Drake',
            'city': 'Vancouver',
            'date': '2024-05-30'
        }

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)

        # Locate Drake Event in Related Events
        self.assertIn(self.event1, response.context['relatedEvents'])

        # See if SearchedFigures is Empty
        self.assertEqual(len(response.context['searchedFigures']), 0)

    # TEST: Handle City
    def test_search_results_only_city(self):

        Query = {
            'city': 'Vancouver'
        }

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)

        # See if Both Events/Figures are in Related Events/Figures
        self.assertIn(self.event1, response.context['relatedEvents'])
        self.assertIn(self.event2, response.context['relatedEvents'])
        self.assertIn(self.figure1, response.context['relatedFigures'])
        self.assertIn(self.figure2, response.context['relatedFigures'])
        
     # TEST: Handle Date + Keyword
    def test_search_results_date_and_query(self):
        # Prepare query parameters
        Query = {
            'date': '2024-05-30',
            'searchQuery': 'Drake'
        }

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)


    # TEST: Handle City + Date
    def test_search_results_city_and_date(self):

        Query = {
            'city': 'Vancouver',
            'date': '2024-05-30'
        }

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)  
        
    # TEST: Handle City + Keyword
    def test_search_results_city_and_query(self):
        Query = {
            'city': 'Vancouver',
            'searchQuery': 'Drake'
        }

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)
        
    #TEST: Handle all EMPTY VALUES
    def test_search_results_empty_case(self):

        Query = {}

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)
        
    #TEST: Handle ONLY DATE
    def test_search_results_date_only(self):
        
        # Create a TIME in the future and set the event to this date
        timeAhead = (timezone.now() + timezone.timedelta(days=7)).date()
        eventAhead = Event.objects.create(eventName='Test Event', eventDate=timeAhead, eventTime='20:00',
                                            eventLocation='Test Location', eventDescription='Test Description',
                                            eventStatus='Active', arenaId=self.arena, figureId=self.figure1)

        Query = {
            'date': timeAhead.strftime('%Y-%m-%d')
        }

        response = self.client.get(reverse('search_results'), Query)
        self.assertEqual(response.status_code, 200)

        # See if this created event is in the Related Events.
        self.assertIn(eventAhead, response.context['relatedEvents'])
    
    #TEST : Handle ONLY KEYWORD
    def test_search_results_query_only(self):

        Query = 'NoFigure'

        response = self.client.get(reverse('search_results'), {'searchQuery': Query})
        self.assertEqual(response.status_code, 200)

        # See if ALL are empty
        self.assertFalse(response.context['searchedFigures'])
        self.assertFalse(response.context['relatedEvents'])
        self.assertFalse(response.context['relatedFigures'])
        
    #TEST : Handle EXACT KEYWORD
    def test_search_results_query_exact(self):
        
        Query = 'Drake'

        response = self.client.get(reverse('search_results'), {'searchQuery': Query})
        self.assertEqual(response.status_code, 200)

        # See if searchedFigures contains DRAKE
        figures = Figure.objects.filter(figureName__icontains=Query)
        for figure in figures:
            self.assertIn(figure, response.context['searchedFigures'])

        # Searched Figure to only show the related figures to the events.
        if figures:
            initialFigure = figures.first()
            relatedEvents = Event.objects.filter(figureId=initialFigure)
            for event in relatedEvents:
                self.assertIn(event, response.context['relatedEvents'])

        # The relatedFigures should only be based on the initialFigures GENRE
        if figures:
            initialFigure = figures.first()
            relatedFigures = Figure.objects.filter(figureGenre=initialFigure.figureGenre).exclude(id=initialFigure.id)
            for figure in relatedFigures:
                self.assertIn(figure, response.context['relatedFigures'])
                
    # TEST: Handle ONLY KEYWORD (Genre)
    def test_search_results_query_only_genre(self):

        Genre = 'Pop'

        response = self.client.get(reverse('search_results'), {'searchQuery': Genre})
        self.assertEqual(response.status_code, 200)

        # Find if Related events with the given Genre exist
        expectedEvents = Event.objects.filter(figureId__figureGenre__iexact=Genre)
        self.assertQuerysetEqual(response.context['relatedEvents'], expectedEvents)

        # Find if Related Figures with the found events exist
        expectedFigures = Figure.objects.filter(event__in=expectedEvents).distinct()
        self.assertQuerysetEqual(response.context['relatedFigures'], expectedFigures)

        # LEAVE SEARCH FIGURE EMPTY
        self.assertFalse(response.context['searchedFigures'])
        
    # TEST: Handle ONLY KEYWORD (MAPPING Genre - rap -> Hip-Hop)
    def test_search_results_query_mapped_genre(self):
        # Define the user input and the mapped genre
        Query = 'rap'
        genreMap = {'rap': 'Hip-Hop'}

        # Find out if the users input will match the genre map
        if Query.lower() in genreMap:
            genreMap = genreMap[Query.lower()]  
            genreFigures = Figure.objects.filter(figureGenre__icontains=genreMap)

            response = self.client.get(reverse('search_results'), {'searchQuery': Query})
            self.assertEqual(response.status_code, 200)

            # See if the figure displayed is the one corresponding to the genre map
            # Should display a rap artist as Hip-Hop is mapped to "rap"
            for figure in genreFigures:
                self.assertIn(figure, response.context['relatedFigures'])
        
    # Login view test
    class LoginViewTest(TestCase):
        def setUp(self):
            # Create a test user
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.client = Client()

        def test_authenticated_user_redirected(self):
            # Log in the user
            self.client.login(self.user)
            response = self.client.get('/login/')
            self.assertRedirects(response, '/', fetch_redirect_response=False)

        def test_login_success(self):
            # Test login with correct credentials
            response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
            assert response.wsgi_request.user.is_authenticated()

        def test_login_failure(self):
            # Test login with incorrect credentials
            response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
            assert response.wsgi_request.user.is_authenticated()

    class LogoutPageViewTest(TestCase):

        def setUp(self):
            # Create a test user
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.client = Client()

        def test_logged_in_user_logs_out(self):
            # Log in the user
            self.client.force_login(self.user)
            # Make a GET request to the logout page
            response = self.client.get('/logout/')
            # Assert that the user is logged out
            self.assertNotIn('_auth_user_id', self.client.session)
            # Assert that the user is redirected to the login page
            self.assertRedirects(response, '/login/')