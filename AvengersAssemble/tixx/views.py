from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Figure
from django.utils import timezone
from django.contrib import admin
from django.urls import path, include
from tixx import views as v
from .models import Event, Ticket, Review
from django.shortcuts import redirect
from django.http import JsonResponse

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


def get_ticket_data(request):
    tickets = Ticket.objects.all().values('ticketId', 'eventId', 'seatNum', 'arenaId', 'ticketQR', 'ticketPrice', 'ticketType', 'zone', 'available')
    return JsonResponse({'tickets': list(tickets)})

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

def figure(request, figure_name):
    figure_case = figure_name.lower()
    figure = get_object_or_404(Figure, figureName__iexact=figure_case)
    
    events = Event.objects.filter(figureId=figure, eventDate__gte=timezone.now()).order_by('eventDate', 'eventTime')
    reviews = Review.objects.filter(reviewFigure=figure)
    
    reviewWithImage = []
    reviewNoImage = []
    for review in reviews:
        if review.reviewimage_set.exists():
            reviewWithImage.append(review)
        else:
            reviewNoImage.append(review)

    return render(request, 'figure.html', {
        'figure': figure,
        'events': events,
        'allReviews': reviewWithImage  + reviewNoImage,
        'reviewCount': len(reviewWithImage) + len(reviewNoImage),
    })

def guest_organiser(request):
    if request.method == 'POST':
        form = GuestOrganiserForm(request.POST)
        if form.is_valid():
            return redirect('some_view_name')  
    else:
        form = GuestOrganiserForm()  
    return render(request, 'guest_organiser.html', {'form': form})