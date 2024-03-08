
from django.db import models

# Create your models here.


class Event(models.Model):
    eventName = models.CharField(max_length=100, default="No Name provided")
    eventDate = models.DateField()
    eventId = models.CharField(primary_key=True, max_length=5)
    eventLocation = models.CharField(max_length=100)
    eventDescription = models.CharField(max_length=250, default="No description provided")
    eventStatus = models.CharField(max_length=10, default="No status provided")


    def __str__(self):
        return self.eventId

class Ticket(models.Model):
    ticketId = models.IntegerField(primary_key=True)
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    seatNum = models.CharField(max_length=5)
    ticketQR = models.CharField(max_length=250)
    ticketPrice = models.IntegerField()
    ticketType = models.CharField(max_length=10)

    def __str__(self):
        return str(self.ticketId)


class User(models.Model):
    userId = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    userEmail = models.EmailField()
    userPhoneNumber = models.IntegerField()
    userAddress = models.CharField(max_length=100)


    def __str__(self):
        return self.userId

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
    reviewId = models.CharField(max_length=10, primary_key=True) # autofield sets it to a primary key automatically 
    reviewRating = models.IntegerField()
    reviewTitle = models.CharField(max_length=10)
    reviewText = models.CharField(max_length=50)
    eventID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reviewDate = models.DateField()

    def __str__(self):
        return self.reviewId

