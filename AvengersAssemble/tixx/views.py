from django.shortcuts import render, HttpResponse
from .models import Event

# Create your views here.

def home(request):
    return render(request, "home.html")

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})