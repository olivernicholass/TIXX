from django.db import models

# Create your models here

class Event(models.Model):
    eventName = models.CharField(max_length=100)
    eventDate = models.DateField()
    eventId = models.AutoField(primary_key=True)
    eventLocation = models.CharField(max_length=100)
    eventDescription = models.CharField(max_length=250)
    eventStatus = models.CharField(max_length=10)
    eventGenre = models.CharField(max_length=100)  
    eventImage = models.ImageField(upload_to='event_images/', null=True, blank=True)  # Added ability to upload images.

    def __str__(self):
        return self.eventName

class Ticket(models.Model):
    ticketId = models.AutoField(primary_key=True)  
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)  
    seatNum = models.CharField(max_length=5)
    ticketQR = models.CharField(max_length=250)
    ticketPrice = models.IntegerField()
    ticketType = models.CharField(max_length=10)
    zone = models.IntegerField(default=1) #1 to 8
    available = models.BooleanField(default=True)

    def get_available_tickets(self):
        total_available = self.objects.filter(sold=True).count()
        total_unavailable = self.objects.filter(sold=False).count()

    def __str__(self):
        return self.seatNum 

class User(models.Model):
    userId = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    userEmail = models.EmailField()
    userPhoneNumber = models.CharField(max_length=10)  
    userAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.username 

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
    reviewTitle = models.CharField(max_length=10)
    reviewText = models.CharField(max_length=50)
    eventID = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True) 
    reviewDate = models.DateField()

    def __str__(self):
        return self.reviewTitle  
