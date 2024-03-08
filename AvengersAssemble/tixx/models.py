from django.db import models

# Create your models here

class Event(models.Model):
    eventName = models.CharField(max_length=100)
    eventDate = models.DateField()
    eventId = models.AutoField(primary_key=True)  # IntegerField to AutoField
    eventLocation = models.CharField(max_length=100)
    eventDescription = models.CharField(max_length=250)
    eventStatus = models.CharField(max_length=10)

    def __str__(self):
        return self.eventName  # Needed to return correct attribute

class Ticket(models.Model):
    ticketId = models.AutoField(primary_key=True)  #  IntegerField to AutoField
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)  # null=True
    seatNum = models.CharField(max_length=5)
    ticketQR = models.CharField(max_length=250)
    ticketPrice = models.IntegerField()
    ticketType = models.CharField(max_length=10)

    def __str__(self):
        return self.seatNum  # Needed to return correct attribute

class User(models.Model):
    userId = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    userEmail = models.EmailField()
    userPhoneNumber = models.CharField(max_length=10)  # IntegerField to CharField
    userAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.username  # Needed to return correct attribute

class Payment(models.Model):
    paymentId = models.CharField(max_length=10, primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # null=True
    paymentAmount = models.FloatField()
    paymentMethod = models.CharField(max_length=10)
    paymentDate = models.DateField()
    transactionId = models.CharField(max_length=10)

    def __str__(self):
        return self.paymentId  # Needed to return correct attribute

class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    reviewRating = models.IntegerField()
    reviewTitle = models.CharField(max_length=10)
    reviewText = models.CharField(max_length=50)
    eventID = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)  # null=True
    reviewDate = models.DateField()

    def __str__(self):
        return self.reviewTitle  # Needed to return correct attribute

class Seat(models.Model):
    seatId = models.AutoField(primary_key=True)
    ticketId = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
    seatNumber = models.IntegerField()

    def __str__(self):
        return self.seatNumber 

