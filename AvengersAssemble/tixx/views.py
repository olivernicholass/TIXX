from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Arena, Event, Figure, ReviewImage, Review
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.urls import path, include
from tixx import views as v
from django.db.models import Avg
from .models import Event, Ticket, Review, User
from django.shortcuts import redirect
from django.http import JsonResponse
from .forms import CreateEventForm, ReviewForm, ReviewImageForm, UserRegistrationForm, OrganiserRegistrationForm
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import user_passes_test

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
    viewedIDS = request.session.get('recently_viewed', [])
    viewedEvents = Event.objects.filter(eventId__in=viewedIDS)

    return render(request, "home.html", {'events': events, 
                                         'carouselFigures': carouselFigures,
                                         'hipHopFigures': hipHopFigures,
                                         'popFigures': popFigures,
                                         'basketballFigures': basketballFigures,
                                         'recently_viewed_events': viewedEvents})
    
def getRecentlyViewed(request, figureId):
    viewedList = request.session.get('recently_viewed', [])

    if figureId not in viewedList:
        viewedList.append(figureId)
        viewedList = viewedList[-3:]  

        request.session['recently_viewed'] = viewedList

    return viewedList

def organiser_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_authenticated and user.isOrganiser:
            auth_login(request, user)
            return redirect('create_event')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'organiser_login.html')

def organiser_register(request):
    if request.method == 'POST':
        organiserForm = OrganiserRegistrationForm(request.POST)
        if organiserForm.is_valid():
            username = organiserForm.cleaned_data.get('username')
            password = organiserForm.cleaned_data.get('password')
            hashPASS = make_password(password)
            if User.objects.filter(username=username).exists():
                messages.error(request, 'A user with that username already exists.')
            else:
                organiser = organiserForm.save(commit=False)
                organiser.password = hashPASS
                organiser.isOrganiser = True
                organiser.save()
                messages.success(request, 'Organiser registered successfully. Please login.')
                return redirect('organiser_login')
        else:
            messages.error(request, 'Invalid form submission. Please check the form data.')
    else:
        organiserForm = OrganiserRegistrationForm()
    return render(request, 'organiser_register.html', {'form': organiserForm })


def isOrganiser(user):
    return user.is_authenticated and user.isOrganiser

@login_required
@user_passes_test(isOrganiser)
def create_event(request):
    
    genres = Figure.objects.values_list('figureGenre', flat=True).distinct()
    arenas = Arena.objects.values_list('arenaName', flat=True).distinct()
    figures = Figure.objects.all()
          
    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CreateEventForm()
        
    return render(request, 'create_event.html', {'form': form, 
                                                 'genres': genres,
                                                 'arenas': arenas,
                                                 'figures': figures})

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

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field '{field}': {error}")
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register.html', {'form': form})

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

def filtered_events(request, eventGenre):
    filtered_events = Event.objects.filter(eventGenre=eventGenre)
    return render(request, 'filtered_events.html', {'filtered_events': filtered_events})

def figure(request, figure_name):
    figure_case = figure_name.lower()
    figure = get_object_or_404(Figure, figureName__iexact=figure_case)
    
    events = Event.objects.filter(figureId=figure, eventDate__gte=timezone.now()).order_by('eventDate', 'eventTime')
    reviews = Review.objects.filter(reviewFigure=figure)
    getRecentlyViewed(request, figure.id)
    
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
    

def get_ticket_data(request):
    tickets = Ticket.objects.all().values('ticketId', 'eventId', 'seatNum', 'arenaId', 'ticketQR', 'ticketPrice', 'ticketType', 'zone', 'available')
    return JsonResponse({'tickets': list(tickets)})

def confirmation(request):
    context = {}
    # if request.method == 'POST':
    #     paymentId = request.POST.get('paymentId')
    #     username = request.POST.get('username')
    #     paymentAmount = request.POST.get('paymentAmount')
    #     paymentMethod = request.POST.get('paymentMethod')
    #     paymentDate = request.POST.get('paymentDate')
    #     transactionId = request.POST.get('transactionId')
    #     ticketId = request.POST.get('ticketId')
    #     seatNum = request.POST.get('seatNum')



    # context = {
    #     'paymentId':paymentId,
    #     'username':username,
    #     'paymentAmount':paymentAmount,
    #     'paymentMethod':paymentMethod,
    #     'paymentDate':paymentDate,
    #     'transactionId':transactionId,
    #     'ticketId': ticketId,
    #     'seatNum': seatNum,
    # }
    return render(request, "confirmation.html",context)
