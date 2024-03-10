from django.shortcuts import render
from .models import Event
from django.shortcuts import redirect
# Create your views here.

def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def profile(request):
    return render(request, "profile.html")

def register(request):
    return render(request, "register.html")

def search_results(request):
    return render(request, "search_results.html")

def ticket_selection(request):
    return render(request, "ticket_selection.html")

def checkout(request):
    return render(request, "checkout.html")

def filtered_events(request, eventGenre):
    filtered_events = Event.objects.filter(eventGenre=eventGenre)
    return render(request, 'filtered_events.html', {'filtered_events': filtered_events})

def figure(request):
    return render(request, "figure.html")