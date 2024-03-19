from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Event, Figure
from django.utils import timezone
# Create your views here.

def home(request):
    events = Event.objects.all()  
    return render(request, "home.html", {'events': events})

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
    return render(request, "ticket_selection.html")

def checkout(request):
    return render(request, "checkout.html")

def filtered_events(request, eventGenre):
    filtered_events = Event.objects.filter(eventGenre=eventGenre)
    return render(request, 'filtered_events.html', {'filtered_events': filtered_events})

def figure(request, figure_name):
    figureCase = figure_name.lower()
    figure = get_object_or_404(Figure, figureName__iexact=figureCase)
    events = Event.objects.filter(figureId=figure, eventDate__gte=timezone.now()).order_by('eventDate', 'eventTime')

    return render(request, 'figure.html', {'figure': figure, 'events': events})