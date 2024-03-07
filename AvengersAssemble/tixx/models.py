from django.db import models

# Create your models here.

class Event(models.Model):
    eventName = models.CharField(max_length=100)
    eventDate = models.DateField()
    eventId = models.IntegerField(max_length=10 ,primary_key=True)
    eventLocation = models.CharField(max_length=100)
    eventDescription = models.CharField(max_length=250)
    eventStatus = models.CharField(max_length=10)


    def __str__(self):
        return self.title

class Ticket(models.Model):
    ticketId = models.IntegerField(max_length=10, primary_key=True)
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL)
    seatNum = models.CharField(max_length=5)
    ticketQR = models.CharField(max_length=250)
    ticketPrice = models.IntegerField()
    ticketType = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class User(models.Model):
    userId = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    userEmail = models.EmailField()
    userPhoneNumber = models.IntegerField(max_length=10)
    userAddress = models.CharField(max_length=100)


    def __str__(self):
        return self.title

class Payment(models.Model):
    paymentId = models.CharField(max_length=10, primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.SET_NULL)
    paymentAmount = models.FloatField()
    paymentMethod = models.CharField(max_length=10)
    paymentDate = models.DateField()
    transactionId = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Review(models.Model):
    reviewId = models.AutoField() # autofield sets it to a primary key automatically 
    reviewRating = models.IntegerField()
    reviewTitle = models.CharField(max_length=10)
    reviewText = models.CharField(max_length=50)
    eventID = models.ForeignKey(User, on_delete=models.SET_NULL)
    reviewDate = models.DateField()

    def __str__(self):
        return self.title

