# admin.py
from django.contrib import admin
from .models import Event, Ticket, User, Payment, Review, Admin, Figure, Arena, ReviewImage

admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Admin)
admin.site.register(Figure)  
admin.site.register(Arena)   
admin.site.register(ReviewImage)
