from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Event, Figure, ReviewImage, Review
from django.utils import timezone
from django.contrib import admin
from django.urls import path, include
from tixx import views as v
from django.db.models import Avg
from .models import Event, Ticket, Review
from django.shortcuts import redirect
from django.http import JsonResponse
from .forms import ReviewForm, ReviewImageForm, GuestOrganiserForm
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date

# Create your views here.

def home(request):
    searchQuery = None
    if request.method == 'GET' and 'searchQuery' in request.GET:
        searchQuery = request.GET.get('searchQuery').lower()
    
    if searchQuery:
        events = Event.objects.filter(eventName__icontains=searchQuery).exclude(eventImage__isnull=True).exclude(eventImage__exact='')
    else:
        events = Event.objects.exclude(eventImage__isnull=True).exclude(eventImage__exact='')

    carouselFigures = Figure.objects.filter(figureName__in=['Queen', 'Ye', 'Frank Ocean'])

    hipHopFigures = Figure.objects.filter(figureGenre='Hip-Hop')
    popFigures = Figure.objects.filter(figureGenre='Pop')
    basketballFigures = Figure.objects.filter(figureGenre='Basketball')

    return render(request, "home.html", {'events': events, 
                                         'carouselFigures': carouselFigures,
                                         'hipHopFigures': hipHopFigures,
                                         'popFigures': popFigures,
                                         'basketballFigures': basketballFigures})

def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else: 

        if request.method == "POST":
            name = request.POST.get("username")
            passwd = request.POST.get("password")
            user = authenticate(request, username=name, password=passwd)
            if user is not None:
                auth_login(request, user)
                return redirect("/")
            else:
                return redirect("/login")
      
    return render(request, "login.html")

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/login")

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
    query = request.GET.get('searchQuery', '').strip()
    city = request.GET.get('city')
    date = request.GET.get('date')
    
    figures = Figure.objects.filter(figureName__icontains=query)
    exactFigures = figures.filter(figureName__iexact=query)
    partialFigures = figures.exclude(figureName__iexact=query)
    
    searchedFigures = []
    relatedFigures = []
    relatedEvents = Event.objects.none()    
    
    # Search Functionality: Handle City + Date + Keyword 
    # - Display EXACT Events for the EXACT Date for the EXACT Figure
    # - i.e City: Vancouver Date: 2024-05-30 Keyword: Drake
    # - Displays events for this exact city, date, and person
    # - Will display other events for other figures if they are also on the same date
    
    if city and date and query:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        cityEvents = Event.objects.filter(eventLocation__iexact=city, eventDate=dateStripped, figureId__figureName__iexact=query)
        relatedFigures = Figure.objects.filter(event__in=cityEvents).distinct()
        relatedEvents = cityEvents
        searchedFigures = []  

    # Search Functionality: Handle City + Date 
    # - Display events only on the EXACT DATE INPUT + Related Figures for those exact events
    
    elif city and date:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        relatedEvents = Event.objects.filter(eventLocation__iexact=city, eventDate=dateStripped)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()

    # Search Functionality: Handle City + Keyword
    # - Display events ONLY related to the specific CITY and the Related Figures to these events.
    # - Empty Searched Figure to only show the related figures to the events.
    
    elif city and query:
        cityEvents = Event.objects.filter(eventLocation__iexact=city, figureId__figureName__iexact=query)
        relatedFigures = Figure.objects.filter(event__in=cityEvents).distinct()
        relatedEvents = cityEvents
        searchedFigures = []  
        
    # Search Functionality: Handle Date + Keyword
    # - Display events only on the EXACT DATE INPUT for the Figure Searched
    # - i.e User puts in 2024-05-30 "Drake", ONLY Drake Concerts show for this date
    # - Empty Searched Figure to only show specific EVENT for specific FIGURE

    elif date and query:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        relatedEvents = Event.objects.filter(eventDate=dateStripped, figureId__figureName__iexact=query)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()

    # Search Functionality: Handling Only City 
    # - Display events based on Event Location, Display Related Figures to these events.
    
    elif city:
        relatedEvents = Event.objects.filter(eventLocation__iexact=city)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()

    # Search Functionality: Handling ONLY DATE 
    # - User searches by only date: Displays events on that date + Related Figures for the events 
    
    elif date:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        relatedEvents = Event.objects.filter(eventDate=dateStripped)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()


    # Search Functionality: Handling ONLY KEYWORD 
    # - User searches by keyword: Example, we have two figures "Frank Ocean" and "Frank Sinatraa"
    # - Display both figures in "Searched Figure" section as they both contain "Frank" 
    # - Related Figures will display based on initialFigure's Genre, so in this case Frank Ocean is first and genre=Pop so other "Pop" Artists
    # - ONLY Search by keyword should show searched figures, rest should display related figures.


    elif query:
  
        # If a user searches only by genre, i.e "Pop" then we retrieve the query 
        # and display the events corresponding to Pop, and then we display
        # the Related Figures that correspond with these events
        # We only display Pop artists that HAVE ACTIVE Events
        # Handle case where user enters Rap, we can receive it from "Hip-Hop/Rap"
   
        genreMap = {
            'rap': 'Hip-Hop',
        }

        # Find if the users input matches our genre mapping, i.e if they enter "rap", it should return "Hip-Hop"
        if query.lower() in genreMap:
            genreMap = genreMap[query.lower()]
            genreFigures = Figure.objects.filter(figureGenre__icontains=genreMap)
        else:
            genreFigures = Figure.objects.filter(figureGenre__icontains=query)

        if genreFigures.exists():
            relatedEvents = Event.objects.filter(figureId__in=genreFigures)
            relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()
            searchedFigures = []

            return render(request, "search_results.html", {'searchedFigures': searchedFigures,
                                                        'relatedFigures': relatedFigures,
                                                        'relatedEvents': relatedEvents})
        else:
            searchedFigures = figures
            if exactFigures:
                initialFigure = exactFigures[0]
                relatedEvents = Event.objects.filter(figureId=initialFigure)
                relatedFigures = Figure.objects.filter(figureGenre=initialFigure.figureGenre).exclude(id=initialFigure.id)
                searchedFigures = exactFigures | partialFigures
            else:
                searchedFigures = figures.distinct()
                if searchedFigures.exists():
                    initialFigure = searchedFigures.first()
                    relatedFigures = Figure.objects.filter(figureGenre=initialFigure.figureGenre).exclude(id=initialFigure.id)
                    relatedEvents = Event.objects.filter(figureId=initialFigure)

    return render(request, "search_results.html", {'searchedFigures': searchedFigures, 
                                                            'relatedFigures': relatedFigures, 
                                                            'relatedEvents': relatedEvents})
def ticket_selection(request):
    row_range = range(10)
    col_range = range(20)
    tickets = Ticket.objects.all()
    
    return render(request, "ticket_selection.html", {'tickets': tickets, 'row_range': row_range, 'col_range': col_range})

def checkout(request):
    return render(request, "checkout.html")

def confirmation(request):
    context = {}
    if request.method == 'POST':
        paymentId = request.POST.get('paymentId')
        username = request.POST.get('username')
        paymentAmount = request.POST.get('paymentAmount')
        paymentMethod = request.POST.get('paymentMethod')
        paymentDate = request.POST.get('paymentDate')
        transactionId = request.POST.get('transactionId')
        ticketId = request.POST.get('ticketId')
        seatNum = request.POST.get('seatNum')

    context = {
        'paymentId':paymentId,
        'username':username,
        'paymentAmount':paymentAmount,
        'paymentMethod':paymentMethod,
        'paymentDate':paymentDate,
        'transactionId':transactionId,
        'ticketId': ticketId,
        'seatNum': seatNum,
    }
    return render(request, "confirmation.html",context)

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

    avgRating = reviews.aggregate(Avg('reviewRating'))['reviewRating__avg']
    if avgRating is not None:
        avgRating = round(avgRating, 1)

    galleryCount = sum(1 for review in reviewWithImage)

    return render(request, 'figure.html', {
        'figure': figure,
        'events': events,
        'allReviews': reviewWithImage + reviewNoImage,
        'reviewCount': len(reviewWithImage) + len(reviewNoImage),
        'averageRating': avgRating,
        'figureName': figure.figureName,
        'galleryCount': galleryCount,  
    })

def review(request, figure_name):
    figure_case = figure_name.lower()
    figure = get_object_or_404(Figure, figureName__iexact=figure_case)
    reviews = Review.objects.filter(reviewFigure=figure)
    
    avgRating = reviews.aggregate(Avg('reviewRating'))['reviewRating__avg']
    if avgRating is not None:
        avgRating = round(avgRating, 1)

    formValidity = False

    if request.method == 'POST':
        reviewForm = ReviewForm(request.POST)
        imageForm = ReviewImageForm(request.POST, request.FILES)
        if reviewForm.is_valid() and imageForm.is_valid():
            review = reviewForm.save(commit=False)
            review.reviewFigure = figure
            review.save()
            for image in request.FILES.getlist('reviewImage'):
                ReviewImage.objects.create(review=review, reviewImage=image)
                
            formValidity = True
            
            return render(request, 'review.html', {
                'figure': figure,
                'averageRating': avgRating,
                'reviewForm': reviewForm,
                'imageForm': imageForm,
                'formValidity': formValidity,
                'figureName': figure.figureName
            })
    else:
        reviewForm = ReviewForm()
        imageForm = ReviewImageForm()  
    
    return render(request, 'review.html', {
        'figure': figure,
        'averageRating': avgRating,
        'reviewForm': reviewForm,
        'imageForm': imageForm,
        'formValidity': formValidity,
        'figureName': figure.figureName 
    })
    
def guest_organiser(request):
    if request.method == 'POST':
        form = GuestOrganiserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = GuestOrganiserForm()  
    return render(request, 'guest_organiser.html', {'form': form})

def get_ticket_data(request):
    tickets = Ticket.objects.all().values('ticketId', 'eventId', 'seatNum', 'arenaId', 'ticketQR', 'ticketPrice', 'ticketType', 'zone', 'available')
    return JsonResponse({'tickets': list(tickets)})
