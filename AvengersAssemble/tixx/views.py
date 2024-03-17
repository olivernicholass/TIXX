from django.shortcuts import render, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from django.urls import path, include
from tixx import views as v
from .models import Event, Ticket
from django.shortcuts import redirect

# Create your views here.

def home(request):
    events = Event.objects.all()  
    return render(request, "home.html", {'events': events})

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def login(request):
    return render(request, "login.html")

def profile(request):
    return render(request, "profile.html")

def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(response, "register.html", {"form":form})

def search_results(request):
    return render(request, "search_results.html")





def ticket_selection(request):
    row_range = range(10)
    col_range = range(20)
    tickets = Ticket.objects.all()
    
    return render(request, "ticket_selection.html", {'tickets': tickets, 'row_range': row_range, 'col_range': col_range})



def checkout(request):
    return render(request, "checkout.html")

def filtered_events(request, eventGenre):
    filtered_events = Event.objects.filter(eventGenre=eventGenre)
    return render(request, 'filtered_events.html', {'filtered_events': filtered_events})

def figure(request):
    return render(request, "figure.html")

