from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title

class User():
    userid = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.username
class ticket():
    ticketid = models.IntegerField()
    eventid = models.models.CharField(max_length=50)
    seatnum = models.CharField(max_length=50)
    QRCode = models.CharField(max_length=50)
    price = models.IntegerField()
    ticketType = models.CharField(max_length=50)
