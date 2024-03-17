from django.db import models

# Create your models here

class Arena(models.Model):
    arenaId = models.CharField(primary_key=True, max_length=5)
    arenaName = models.CharField(max_length=20)
    arenaCapacity = models.IntegerField()

    def __str__(self):
     return self.arenaName


class Event(models.Model):
    eventName = models.CharField(max_length=100)
    eventDate = models.DateField()
    eventId = models.AutoField(primary_key=True) # IntegerField to AutoField
    eventLocation = models.CharField(max_length=100)
    eventDescription = models.CharField(max_length=250)
    eventStatus = models.CharField(max_length=10)
    eventGenre = models.CharField(max_length=100, default="none")  
    eventImage = models.ImageField(upload_to='event_images/', null=True, blank=True)  
    arenaId = models.ForeignKey(Arena,on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.eventName # Needed to return correct attribute

class Ticket(models.Model):
    ticketId = models.AutoField(primary_key=True) # IntegerField to AutoField
    eventId = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True) # null=True
    seatNum = models.CharField(max_length=5)
    arenaId = models.ForeignKey(Arena,on_delete=models.SET_NULL, null=True)
    ticketQR = models.CharField(max_length=250)
    ticketPrice = models.IntegerField()
    ticketType = models.CharField(max_length=10)
    zone = models.IntegerField(default=1) #1 to 8
    available = models.BooleanField(default=True)

    def get_available_tickets(self):
        total_available = self.objects.filter(sold=True).count()
        total_unavailable = self.objects.filter(sold=False).count()

    def __str__(self):
        return self.seatNum # Needed to return correct attribute

class User(models.Model):
    userId = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    userPassword = models.CharField(max_length=20, default='temp_password')
    userEmail = models.EmailField()
    userPhoneNumber = models.CharField(max_length=10) # IntegerField to CharField
    userAddress = models.CharField(max_length=100)

    def __str__(self):
     return self.username # Needed to return correct attribute

class Payment(models.Model):
    paymentId = models.CharField(max_length=10, primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # null=True
    paymentAmount = models.FloatField()
    paymentMethod = models.CharField(max_length=10)
    paymentDate = models.DateField()
    transactionId = models.CharField(max_length=10)

    def __str__(self):
        return self.paymentId # Needed to return correct attribute

class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    reviewRating = models.IntegerField()
    reviewTitle = models.CharField(max_length=10)
    reviewText = models.CharField(max_length=50)
    eventID = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True) # null=True
    reviewDate = models.DateField()

    def __str__(self):
     return self.reviewTitle # Needed to return correct attribute

class Seat(models.Model):
    seatId = models.AutoField(primary_key=True)
    ticketId = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
    seatNumber = models.IntegerField()
    arenaId = models.ForeignKey(Arena,on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.seatNumber 
    
class Figure(models.Model):
    figureName = models.CharField(max_length=100)
    figureGenre = models.CharField(max_length=100)
    figurePicture = models.ImageField(upload_to='figure_images/', null=True, blank=True)

    def __str__(self):
        return self.figureName

class Admin(models.Model):
    adminId = models.AutoField(primary_key=True)
    adminName = models.CharField(max_length=20)
    adminEmail = models.EmailField()
    adminPassword = models.CharField(max_length=20)

    def __str__(self):
     return self.adminName





