from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.title

class User():
    from django import connection
    userid = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def getReviews():
        with connection.cursor() as curson:
            cursor.execute(sql)
            rows = cursor.fetchall()

        #sql to return:
        #SELECT * FROM reviews WHERE userid=(this.userid)

    def getPayments():
    
    def getTickets():
    
    def __str__(self):
        return self.username + ", " + self.email + ", " + self.phone + ", " + self.address + ", " + userid

    def buyTickets():

    def addToCart():

    def deleteFromCart():
        
    def makePayment():

    
    