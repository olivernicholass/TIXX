from django.db import models

# Create your models here

class Arena(models.Model):
    arenaId = models.CharField(primary_key=True, max_length=5)
    arenaName = models.CharField(max_length=50)
    arenaCapacity = models.IntegerField()

    def __str__(self):
     return self.arenaName
 
class Figure(models.Model):
    figureName = models.CharField(max_length=100)
    figureGenre = models.CharField(max_length=100)
    figurePicture = models.ImageField(upload_to='figure_images/', null=True, blank=True)
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
    figureId = models.ForeignKey(Figure, on_delete=models.SET_NULL, null=True)

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

class User(models.Model):
    userId = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    userPassword = models.CharField(max_length=20, default='temp_password')
    userEmail = models.EmailField()
    userPhoneNumber = models.CharField(max_length=10) 
    userAddress = models.CharField(max_length=100)

    def __str__(self):
     return self.username #

class Payment(models.Model):
    paymentId = models.CharField(max_length=10, primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    paymentAmount = models.FloatField()
    paymentMethod = models.CharField(max_length=10)
    paymentDate = models.DateField()
    transactionId = models.CharField(max_length=10)

    def __str__(self):
        return self.paymentId

class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    reviewRating = models.IntegerField()
    reviewTitle = models.CharField(max_length=100)
    reviewText = models.CharField(max_length=500)
    eventID = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
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





