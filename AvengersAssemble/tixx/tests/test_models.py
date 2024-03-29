from django.test import TestCase
from tixx.models import Arena, Event, Ticket, Review, Seat, Figure, Admin, ReviewImage, User

class ModelTestCase(TestCase):
    def setUp(self):
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
            eventDate="2024-03-10",
            eventLocation="Test Location",
            eventDescription="Test Description",
            eventStatus="Upcoming",
            eventGenre="Test Genre",
            arenaId=self.arena,
            figureId=self.figure
        )
        self.ticket = Ticket.objects.create(
            eventId=self.event,
            seatNum="A1",
            arenaId=self.arena,
            ticketQR="test_qr_code",
            ticketPrice=50,
            ticketType="Regular",
            zone=1,
            available=True
        )
        self.review = Review.objects.create(
            reviewRating=5,
            reviewTitle="Great Event",
            reviewText="Drake was great!!!",
            reviewFigure=self.figure,
            reviewDate="2024-03-09"
        )
        self.review_image = ReviewImage.objects.create(
            review=self.review,
            reviewImage="test_image.jpg"
        )
        self.seat = Seat.objects.create(
            ticketId=self.ticket,
            seatNumber="1",
            arenaId=self.arena
        )
        self.admin = Admin.objects.create(
            adminName="Test Admin",
            adminEmail="admin@example.com",
            adminPassword="admin123"
        )
        
    def test_arena_str(self):
        self.assertEqual(str(self.arena), "Test Arena")
        
    def test_event_str(self):
        self.assertEqual(str(self.event), "Test Event")

    def test_ticket_str(self):
        self.assertEqual(str(self.ticket), "A1")

    def test_review_str(self):
        self.assertEqual(str(self.review), "Great Event")
        
    def test_figure_str(self):
        self.assertEqual(str(self.figure), "Test Figure")

    def test_review_image_str(self):
        self.assertEqual(str(self.review_image), f"Image for Review '{self.review.reviewTitle}' - ID: {self.review.reviewId}")
        
    def test_seat_str(self):
        self.assertEqual(str(self.seat), "1")

    def test_admin_str(self):
        self.assertEqual(str(self.admin), "Test Admin")

# NEW USER MODEL TEST CASE

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            userPhoneNumber="1234567890",
            userAddress="Test Address",
            password="test_password"
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "test_user")

    def test_user_is_regular_user_by_default(self):
        self.assertFalse(self.user.isOrganiser)

    def test_user_creation(self):
        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.userPhoneNumber, "1234567890")
        self.assertEqual(self.user.userAddress, "Test Address")
        self.assertFalse(self.user.isOrganiser)
        self.assertTrue(self.user.check_password("test_password"))

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            userPhoneNumber="0987654321",
            userAddress="Admin Address",
            password="admin_password"
        )
        self.assertIsNotNone(superuser)
        self.assertEqual(superuser.username, "admin")
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertEqual(superuser.userPhoneNumber, "0987654321")
        self.assertEqual(superuser.userAddress, "Admin Address")
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.check_password("admin_password"))
