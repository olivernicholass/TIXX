from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
import uuid


# Create your models here

class Arena(models.Model):
    arenaId = models.CharField(primary_key=True, max_length=5)
    arenaName = models.CharField(max_length=50)
    arenaCapacity = models.IntegerField()

    def __str__(self):
     return self.arenaName
 
class Figure(models.Model):
    figureName = models.CharField(max_length=100, unique=True)
    figureGenre = models.CharField(max_length=100)
    figurePicture = models.ImageField(upload_to='figure_images/', null=True, blank=True)
    carouselImage = models.ImageField(upload_to='carousel_images/', null=True, blank=True)
    figureAbout = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.figureName

class Event(models.Model):
    eventName = models.CharField(max_length=100)
    eventDate = models.DateField()
    eventTime = models.TimeField(default='12:00')
    eventId = models.AutoField(primary_key=True) 
    eventLocation = models.CharField(max_length=100)
    eventDescription = models.CharField(max_length=250)
    eventStatus = models.CharField(max_length=10)
    eventGenre = models.CharField(max_length=100, default="none")  
    eventImage = models.ImageField(upload_to='event_images/', null=True, blank=True)  
    arenaId = models.ForeignKey(Arena,on_delete=models.SET_NULL, null=True)
    adminCheck = models.BooleanField(default=False)
    isRejected = models.BooleanField(default=False)
    figureId = models.ForeignKey(Figure, on_delete=models.SET_NULL, null=True)
    organiser = models.ForeignKey('tixx.User', on_delete=models.CASCADE, related_name='events',  null=True)


    def __str__(self):
        return self.eventName
    
class Ticket(models.Model):
    ticketId = models.AutoField(primary_key=True) 
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True) 
    seatNum = models.CharField(max_length=5)
    arenaId = models.ForeignKey(Arena,on_delete=models.SET_NULL, null=True)
    ticketQR = models.CharField(max_length=250)
    ticketPrice = models.IntegerField()
    ticketType = models.CharField(max_length=10)
    zone = models.IntegerField(default=1) #1 to 8
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.seatNum 


# READJUSTED ENTIRE USER MODEL AS A CUSTOM USER MODEL (NOT DJANGO DEFAULT)
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, userPhoneNumber, userAddress, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, userPhoneNumber=userPhoneNumber, userAddress=userAddress, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, userPhoneNumber, userAddress, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, userPhoneNumber, userAddress, password, **extra_fields)

class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    userDescription = models.CharField(max_length=200, blank=True)
    userPhoneNumber = models.CharField(max_length=10, blank=True)
    userAddress = models.CharField(max_length=100, blank=True)
    isOrganiser = models.BooleanField(default=False)
    organiserCredentials = models.CharField(max_length=100, blank=True)
    userProfilePicture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    userProfilePicture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='profile_pictures/default.png')
    miniImage = models.ImageField(upload_to='mini_images/', blank=True, null=True)
    firstName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=150, blank=True)
    favoriteFigure = models.ForeignKey(Figure, on_delete=models.SET_NULL, blank=True, null=True)
    favoriteSongSpotifyId = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    stateProvince = models.CharField(max_length=100, blank=True)
    postalcode = models.CharField(max_length=20, blank=True)

    REQUIRED_FIELDS = ['email', 'userPhoneNumber', 'userAddress']
    
class Payment(models.Model):
    paymentId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True) 
    seatNum = models.ManyToManyField(Ticket, blank=True)
    paymentAmount = models.FloatField()
    paymentMethod = models.CharField(max_length=10)
    paymentDate = models.DateField()
    transactionId = models.CharField(max_length=10)
    firstName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=150, blank=True)
    phoneNumber = models.IntegerField(null=True)
    email = models.EmailField(max_length=20, blank=True)
    Address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
   

    def __str__(self):
        return str(self.paymentId)

class Review(models.Model):
    userReview = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    reviewId = models.AutoField(primary_key=True)
    reviewRating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    reviewTitle = models.CharField(max_length=100)
    reviewText = models.CharField(max_length=500)
    reviewFigure = models.ForeignKey(Figure, on_delete=models.CASCADE, default=None)  
    reviewDate = models.DateField()

    def __str__(self):
        return self.reviewTitle
    
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    reviewImage = models.ImageField(upload_to='review_images/', null=True, blank=True)

    def __str__(self):
        return f"Image for Review '{self.review.reviewTitle}' - ID: {self.review.reviewId}"

class Seat(models.Model):
    seatId = models.AutoField(primary_key=True)
    ticketId = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
    seatNumber = models.IntegerField()
    arenaId = models.ForeignKey(Arena,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.seatNumber 
    

class Admin(models.Model):
    adminId = models.AutoField(primary_key=True)
    adminName = models.CharField(max_length=20)
    adminEmail = models.EmailField()
    adminPassword = models.CharField(max_length=20)

    def __str__(self):
     return self.adminName





