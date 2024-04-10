import os
from django.conf import settings
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.utils import timezone
from tixx.models import Figure, Event, Review, ReviewImage, Arena, User, Ticket, Payment
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.template import Context, Template
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from tixx.views import getRecentlyViewed, review
from tixx.forms import ReviewForm, ReviewImageForm, OrganiserRegistrationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from datetime import date
import datetime
import stripe
from django.http import JsonResponse
import json
from unittest.mock import patch
import uuid
from  tixx.forms import CreateEventForm
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone




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
        
    class viewProfile(TestCase):
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(username='testuser', password='testpassword')

        def test_profile_url(self):
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('view_profile'))
            self.assertEqual(response.status_code, 200)
            
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



    def test_checkout_view(self):
        # Assuming 'selected_seats' is a valid string of selected seats for testing purposes
        event_id = 1
        selected_seats = 'S1A1,S1B2,S1C3'  # Replace with actual selected seats
        response = self.client.get(reverse('checkout', args=[event_id, selected_seats]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')

class TicketSelectionViewTest(TestCase):
    def setUp(self):
        # Create a test Event object

        self.arena = Arena.objects.create(
            arenaId="test_arena",
            arenaName="Test Arena",
            arenaCapacity=2
        )
        self.figure = Figure.objects.create(
            figureName="Test Figure",
            figureGenre="Test Genre",
            figureAbout="Test Description"
        )
        self.event = Event.objects.create(
            eventName="Test Event",
            eventId="1",
            eventDate="2024-03-10",
            eventLocation="Test Location",
            eventDescription="Test Description",
            eventStatus="Upcoming",
            eventGenre="Test Genre",
            arenaId=self.arena,
            figureId=self.figure
        )


    def test_ticket_selection_view(self):
        # Assuming 'eventid' is a valid ID for testing purposes
        event_id = self.event.eventId  # Use the ID of the test event object
        response = self.client.get(reverse('ticket_selection', args=[event_id]))
        self.assertEqual(response.status_code, 200)  # Assuming it should return 200 for existing event
        self.assertTemplateUsed(response, 'ticket_selection.html')

# Filtered Events Test 

class FilteredEventsTestCase(TestCase):
    def setUp(self):
        self.arena = Arena.objects.create(arenaId='A001', arenaName='Test Arena', arenaCapacity=1000)
        self.figure = Figure.objects.create(figureName='Test Figure', figureGenre='Genre-1', figurePicture='Drake.jpg')
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
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',  
            userPhoneNumber='1234567890',  
            userAddress='Test Address'       
        )
        
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
        self.client.login(username='testuser', password='testpassword') 
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
        self.client.login(username='testuser', password='testpassword') 
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
        # TEST FIGURES
        self.figure1 = Figure.objects.create(figureName='Drake', figureGenre='Hip-Hop', figurePicture=self.testJPG)
        self.figure2 = Figure.objects.create(figureName='Adele', figureGenre='Pop', figurePicture=self.testJPG)

        # TEST EVENTS/ARENA
        self.arena = Arena.objects.create(arenaId='12345', arenaName='Test Arena', arenaCapacity=10000)
        self.event1 = Event.objects.create(eventName='Drake Concert', eventDate='2024-05-30', eventTime='20:00',
                                            eventLocation='Vancouver', eventDescription='Concert', eventStatus='Active',
                                            arenaId=self.arena, figureId=self.figure1, adminCheck=True, isRejected=False)
        self.event2 = Event.objects.create(eventName='Adele Concert', eventDate='2024-05-30', eventTime='19:00',
                                            eventLocation='Vancouver', eventDescription='Concert', eventStatus='Active',
                                            arenaId=self.arena, figureId=self.figure2, adminCheck=True, isRejected=False)
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
                                            eventStatus='Active', arenaId=self.arena, figureId=self.figure1, adminCheck=True, isRejected=False)

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
            
# ORGANISER LOGIN + REGISTER TEST CASES (~97% COVERAGE 1 LINE NOT COVERED)

class OrganiserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'
        self.phone_number = '1234567890'
        self.address = '123 Test St'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            userPhoneNumber=self.phone_number,
            userAddress=self.address,
            isOrganiser=True
        )

    # TEST: Organiser can login w/ correct details and gets redirected to the organiser dashboard. This also confirms
    # that the user is recognised as an organiser when logged in.

    def test_organiser_login(self):
        response = self.client.post(reverse('organiser_login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('dashboard_home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.isOrganiser)

    # TEST: This checks that a user with invalid details cannot login and it displays the error meesage, also confirming
    # that they are not authenticated.

    def test_organiser_login_invalid_credentials(self):
        response = self.client.post(reverse('organiser_login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertContains(response, 'Invalid username or password.')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # TEST: This test check that a new organiser can register successfully with all correct details, once registered they are
    # redirected to the organiser login page and this check that the organiser is also register with organiser status.

    def test_organiser_register(self):
        username = 'newuser'
        password = 'newpassword'
        secretKEY = "tixxEVENTORGANISER"
        response = self.client.post(reverse('organiser_register'), {
            'username': username,
            'password': password,
            'isOrganiser': True,
            'organiserCredentials': secretKEY,
            'email': 'newuser@example.com',
            'userPhoneNumber': '1234567890',
            'userAddress': '123 Test St',
            'secretKeyword': secretKEY
        })
        self.assertRedirects(response, reverse('organiser_login'))
        self.assertTrue(User.objects.filter(username=username).exists())
        newUSER = User.objects.get(username=username)
        self.assertTrue(newUSER.isOrganiser)

    # ------------------------------------- MOSTLY EDGE CASES ------------------------------------- #
    # TEST: Asserts that the organiser form is instantiated when the regristration page is opened.

    def test_organiser_register_form_instantiation(self):
        response = self.client.get(reverse('organiser_register'))
        self.assertIsInstance(response.context['form'], OrganiserRegistrationForm)

    # TEST: Checks and confirms that the we are using the correct html template for organiser registration

    def test_organiser_register_render_template(self):
        response = self.client.get(reverse('organiser_register'))
        self.assertTemplateUsed(response, 'organiser_register.html')

    # TEST: Checks that attempting to register with an already existing username/password displays the error message we have in the view

    def test_organiser_register_existing_user_message(self):
        existingUSER = 'existinguser'
        User.objects.create_user(username=existingUSER, email='existing@example.com', password='password', userPhoneNumber='1234567890', userAddress='123 Test St')
        response = self.client.post(reverse('organiser_register'), {'username': existingUSER, 'password': 'password'})
        self.assertContains(response, 'A user with that username already exists.')

    # TEST: Checks that attempting to register with a form that is not filled out, will display the error message we set in the view.

    def test_organiser_register_invalid_form_message(self):
        response = self.client.post(reverse('organiser_register'), {})
        self.assertContains(response, 'This field is required.')

# GET RECENTLY VIEWED TEST (~100% COVERAGE)

User = get_user_model()

class RecentlyViewedTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_getRecentlyViewed(self):
        request = self.factory.get('/')
        request.session = {}

        # Add FIGURE IDS 
        getRecentlyViewed(request, 1)
        getRecentlyViewed(request, 2)
        getRecentlyViewed(request, 3)

        # See if the session was updated correctly
        self.assertEqual(request.session['recently_viewed'], [1, 2, 3])

        # Append another figureId which should remove the previous one.
        getRecentlyViewed(request, 4)
        self.assertEqual(request.session['recently_viewed'], [2, 3, 4])

        # Append a duplicate figureID which should not do anything to the list
        getRecentlyViewed(request, 3)
        self.assertEqual(request.session['recently_viewed'], [2, 3, 4])
        
# GET Figure TEST (recentlytag.py) (~100% COVERAGE)

class GetFigureFilterTestCase(TestCase):
    def setUp(self):
        self.figure = Figure.objects.create()

    def test_getFigure_filter(self):
        template = Template("{% load recentlytag %}{{ figure_id|getFigure }}")
        render = template.render(Context({'figure_id': self.figure.id}))
        self.assertInHTML(str(self.figure), render)
        
# ADMIN REVIEW VIEW TEST (~100% COVERAGE)

class AdminReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', userPhoneNumber='1234567890', userAddress='123 Test St', password='testpassword')
        self.client.login(username='test@example.com', password='testpassword')
        self.user.is_staff = True
        self.user.save()
        self.pending_event = Event.objects.create(
            eventName='Pending Event',
            adminCheck=False,
            isRejected=False,
            eventDate=date.today()
        )
        self.accepted_event = Event.objects.create(
            eventName='Accepted Event',
            adminCheck=True,
            isRejected=False,
            eventDate=date.today()
        )

    def test_admin_review_view(self):
        response = self.client.get(reverse('admin_review'))
        self.assertEqual(response.status_code, 200)

        # COUNTS/EVENTS Passed to template
        self.assertEqual(len(response.context['pendingEvents']), 1)
        self.assertEqual(len(response.context['acceptedEvents']), 1)
        self.assertEqual(len(response.context['rejectedEvents']), 0)
        self.assertEqual(response.context['pendingCount'], 1)
        self.assertEqual(response.context['acceptedCount'], 1)
        self.assertEqual(response.context['rejectedCount'], 0)

        # POST TO Accept and Event
        response = self.client.post(reverse('admin_review'), {'eventId': self.accepted_event.eventId, 'accept': 'Accept'})
        self.assertEqual(response.status_code, 200) 

        # POST to Reject an Event
        response = self.client.post(reverse('admin_review'), {'eventId': self.accepted_event.eventId, 'reject': 'Reject'})
        self.assertEqual(response.status_code, 200) 

        # TEST an Event with a non-existing ID
        response = self.client.post(reverse('admin_review'), {'eventId': 999, 'accept': 'Accept'})

        self.assertEqual(response.status_code, 302)  # Redirects after POST

class CheckoutViewTest(TestCase):
    def setUp(self):
        # Setup test data
        self.client = Client()

        self.arena = Arena.objects.create(
            arenaId='A123',
            arenaName='Main Arena',
            arenaCapacity=5000,
        )
        self.event = Event.objects.create(
            eventName='Event name',
            eventDate='2024-07-04',
            eventTime='17:00:00',
            eventLocation='event location',
            eventDescription='Enjoy an evening of music from top artists from around the world.',
            eventStatus='Status',  
            eventGenre='Music', 
            arenaId=self.arena,
            # Add or adjust fields based on your actual Event model
        )
        # Create some Ticket instances related to the event
        self.ticket1 = Ticket.objects.create(
            eventId=self.event, 
            seatNum="A1", 
            ticketPrice=100,
            ticketType='Standard',
            zone=1,
            available=True,
            arenaId=self.arena,  # Assuming each ticket is associated with an arena
            # The ticketQR field is omitted in this example; include it if required for your tests
        )
        self.ticket2 = Ticket.objects.create(
            eventId=self.event, 
            seatNum="A2", 
            ticketPrice=150,
            ticketType='VIP',
            zone=1,
            available=True,
            arenaId=self.arena,  # Assuming each ticket is associated with an arena
            # The ticketQR field is omitted in this example; include it if required for your tests
        )

        # Generate a URL for testing
        self.checkout_url = reverse('checkout', args=[self.event.pk, "A1,A2"])  # Adjust the URL name and parameters based on your urls.py

    def test_checkout_view(self):
        # Simulate a GET request to the checkout view
        response = self.client.get(self.checkout_url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the response context contains the correct event_id and selected_seat_nums
        self.assertEqual(response.context['event_id'], self.event.eventId)
        self.assertListEqual(response.context['selected_seat_nums'], ["A1", "A2"])

        # Check that the tickets in the context match the tickets created in setUp
        expected_ticket_ids = {self.ticket1.ticketId, self.ticket2.ticketId}
        response_ticket_ids = {ticket.ticketId for ticket in response.context['tickets']}
        self.assertEqual(expected_ticket_ids, response_ticket_ids)

        # Check that the correct template was used
        self.assertTemplateUsed(response, "checkout.html")



        
        
        
# EDIT/VIEW PROFILE VIEW TEST (100% COVERAGE)

class ViewProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_view_profile(self):
        response = self.client.get(reverse('view_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_profile.html')
        self.assertEqual(response.context['user'], self.user)

        # Test to see if the users revies in context match the reviews displaying on the page

        self.assertQuerysetEqual(response.context['reviews'], Review.objects.filter(userReview=self.user), transform=lambda x: x)
        
    def tearDown(self):
        self.client.logout()
        
class EditProfile(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_edit_profile_view(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)

        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'userPhoneNumber': '1234567890',
            'userAddress': '123 Main St',
            'city': 'Anytown',
            'stateProvince': 'ABC',
            'postalcode': '12345',
            'favoriteSongSpotifyId': '1234567890123456789012',
            'userDescription': 'description',
            'username_color': '#03256C',
        }

        # Set the paths for mini_image and pfp
        miniPATH= os.path.join(settings.MEDIA_ROOT, 'mini_images', 'dasdasdasdad.png')
        pfpPATH = os.path.join(settings.MEDIA_ROOT, 'profile_pictures', 'default.png')

        data['mini_image'] = open(miniPATH, 'rb')
        data['pfp'] = open(pfpPATH, 'rb')

        response = self.client.post(reverse('edit_profile'), data)
        self.assertEqual(response.status_code, 302) 

        # Verify data matching
        self.user.refresh_from_db()
        self.assertEqual(self.user.firstName, 'John')
        self.assertEqual(self.user.lastName, 'Doe')
        self.assertEqual(self.user.email, 'john.doe@example.com')

        # Make sure that the review is deleted even if its not in the data
        self.assertEqual(Review.objects.filter(userReview=self.user).count(), 0)

        self.assertTrue('mini_image' in data)
        self.assertTrue(self.user.miniImage.name.startswith('mini_images/'))

        self.assertTrue('pfp' in data)
        self.assertTrue(self.user.userProfilePicture.name.startswith('profile_pictures/'))

        figure = Figure.objects.create(
            figureName="Test Figure",
            figureGenre="Test Genre",
            figureAbout="Test Description"
        )

        review = Review.objects.create(
            userReview=self.user,
            reviewRating=4.5,  
            reviewTitle='Great experience',
            reviewText='Test review text',
            reviewFigure=figure,  
            reviewDate=timezone.now()
        )

        # DELETE the user review
        response = self.client.post(reverse('edit_profile'), {'delete_review': review.reviewId})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Review.objects.filter(userReview=self.user).count(), 0)

        # See if the correct color is in the users session
        self.assertEqual(self.client.session['username_color'], '#03256C')


    def tearDown(self):
        self.client.logout()
       

# class ConfirmationViewTest(TestCase):
#     def setUp(self):
#         # Setup
#         self.event = Event.objects.create(eventName="Test Event", eventDate="2023-05-05")
#         self.ticket1 = Ticket.objects.create(eventId=self.event, seatNum="A1", ticketPrice=100)
#         self.ticket2 = Ticket.objects.create(eventId=self.event, seatNum="A2", ticketPrice=100)

#         self.payment = Payment.objects.create(
#             eventId=self.event,
#             firstName='John',
#             lastName='Doe',
#             phoneNumber='1234567890',
#             email='john@example.com',
#             Address='123 Test St',
#             city='Test City',
#             province='Test Prov',
#             paymentAmount=100,
#             paymentMethod="Stripe",
#             paymentDate="2023-05-01",
#             paymentId=uuid.uuid4()
#         )
#         self.payment.seatNum.add(self.ticket1, self.ticket2)

#     def test_confirmation_page(self):
#         # Execution
#         response = self.client.get(reverse('confirmation', args=[self.payment.paymentId]))

#         # Assertions
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'confirmation.html')
#         self.assertIn('payment', response.context)
#         self.assertEqual(response.context['payment'], self.payment)




        
# ORGANISER dashboard tests

# class EventViewTests(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.organiser = User.objects.create_user(username='organiser', password='12345')
#         self.event = Event.objects.create(
#             organiser=self.organiser, 
#             eventName="Sample Event", 
#             eventDate=timezone.now() + timezone.timedelta(days=30),
#             eventTime="12:00",
#             eventLocation="Sample Location",
#             eventDescription="Sample Description",
#             eventStatus="Upcoming",
#             eventGenre="Sample Genre",
#         )
#         self.client.login(username='organiser', password='12345')
        
#     def test_delete_event_get_request(self):
#         response = self.client.get(reverse('delete_event', args=[self.event.eventId]))  
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'confirm_delete.html')
#         self.assertEqual(response.context['event'], self.event)

#     def test_delete_event_post_request(self):
#         response = self.client.post(reverse('delete_event', args=[self.event.eventId])) 
#         self.assertRedirects(response, reverse('dashboard_home'))
#         self.assertFalse(Event.objects.filter(eventId=self.event.eventId).exists()) 
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(len(messages), 1)
#         self.assertIn('Event deleted successfully!', str(messages[0]))

