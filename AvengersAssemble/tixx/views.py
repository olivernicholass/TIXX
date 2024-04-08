from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Arena, Event, Figure, ReviewImage, Review, Payment
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.utils import timezone
from django.contrib import admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password
from django.urls import path, include, reverse
from tixx import views as v
from django.db.models import Avg
from .models import Event, Ticket, Review, User
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from .forms import CreateEventForm, EditProfileForm, ReviewForm, ReviewImageForm, UserRegistrationForm, OrganiserRegistrationForm
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.utils.dateparse import parse_date
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import user_passes_test
import stripe
from django.conf import settings
import uuid


def home(request):
    searchQuery = None
    if request.method == 'GET' and 'searchQuery' in request.GET:
        searchQuery = request.GET.get('searchQuery').lower()
    
    if searchQuery:
        events = Event.objects.filter(eventName__icontains=searchQuery, adminCheck=True).exclude(eventImage__isnull=True).exclude(eventImage__exact='')
    else:
        events = Event.objects.filter(adminCheck=True).exclude(eventImage__isnull=True).exclude(eventImage__exact='')

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

def admin_review(request):
    if request.method == 'POST':
        eventId = request.POST.get('eventId')

        if eventId is not None:
            try:
                event = Event.objects.get(pk=eventId)
            except Event.DoesNotExist:
                messages.error(request, f"Event with id {eventId} does not exist.")
                return redirect('admin_review')

            if 'accept' in request.POST:
                event.adminCheck = True
                event.isRejected = False
                event.save()
            elif 'reject' in request.POST:
                event.isRejected = True
                event.adminCheck = False
                event.save()

    # COUNTS of pending/accepted/rejected events
    pendingCount = Event.objects.filter(adminCheck=False, isRejected=False).count()
    acceptedCount = Event.objects.filter(adminCheck=True, isRejected=False).count()
    rejectedCount = Event.objects.filter(adminCheck=False, isRejected=True).count()

    # ALL pending/accepted/rejected events
    pendingEvents = Event.objects.filter(adminCheck=False, isRejected=False)
    acceptedEvents = Event.objects.filter(adminCheck=True, isRejected=False)
    rejectedEvents = Event.objects.filter(adminCheck=False, isRejected=True)

    return render(request, 'admin_review.html', {
        'pendingEvents': pendingEvents,
        'acceptedEvents': acceptedEvents,
        'rejectedEvents': rejectedEvents,
        'pendingCount': pendingCount,
        'acceptedCount': acceptedCount,
        'rejectedCount': rejectedCount,
    })
    
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
    arenas = Arena.objects.all()
    figures = Figure.objects.all()

    if request.method == 'POST':
        form = CreateEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.adminCheck = False
            arena_id = request.POST.get('arenaId')  
            arena = Arena.objects.get(pk=arena_id) 
            event.arenaId = arena
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
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

@login_required
def view_profile(request):
    user = request.user 
    reviews = Review.objects.filter(userReview=user)
    return render(request, 'view_profile.html', {'user': user, 'reviews': reviews})

@login_required
def edit_profile(request):
    reviews = Review.objects.filter(userReview=request.user)
    user = request.user
    form = EditProfileForm(request.POST or None, request.FILES or None, initial={
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email,
        'userPhoneNumber': user.userPhoneNumber,
        'userAddress': user.userAddress,
        'city': user.city,
        'stateProvince': user.stateProvince,
        'postalcode': user.postalcode,
        'favoriteSongSpotifyId': user.favoriteSongSpotifyId,
        'userDescription': user.userDescription,
    })
    if request.method == 'POST' and form.is_valid():
        if 'firstName' in form.cleaned_data and form.cleaned_data['firstName']:
            user.firstName = form.cleaned_data['firstName']
        if 'lastName' in form.cleaned_data and form.cleaned_data['lastName']:
            user.lastName = form.cleaned_data['lastName']
        if 'email' in form.cleaned_data and form.cleaned_data['email']:
            user.email = form.cleaned_data['email']
        if 'userPhoneNumber' in form.cleaned_data and form.cleaned_data['userPhoneNumber']:
            user.userPhoneNumber = form.cleaned_data['userPhoneNumber']
        if 'userAddress' in form.cleaned_data and form.cleaned_data['userAddress']:
            user.userAddress = form.cleaned_data['userAddress']
        if 'city' in form.cleaned_data and form.cleaned_data['city']:
            user.city = form.cleaned_data['city']
        if 'stateProvince' in form.cleaned_data and form.cleaned_data['stateProvince']:
            user.stateProvince = form.cleaned_data['stateProvince']
        if 'postalcode' in form.cleaned_data and form.cleaned_data['postalcode']:
            user.postalcode = form.cleaned_data['postalcode']
        if 'favoriteSongSpotifyId' in form.cleaned_data and form.cleaned_data['favoriteSongSpotifyId']:
            user.favoriteSongSpotifyId = form.cleaned_data['favoriteSongSpotifyId']
        if 'userDescription' in form.cleaned_data and form.cleaned_data['userDescription']:
            user.userDescription = form.cleaned_data['userDescription']
        if 'mini_image' in form.cleaned_data and form.cleaned_data['mini_image']:
            mini_image = form.cleaned_data['mini_image']
            file_name = default_storage.save('mini_images/' + mini_image.name, ContentFile(mini_image.read()))
            user.miniImage = file_name
        if 'pfp' in form.cleaned_data and form.cleaned_data['pfp']:
            pfp_image = form.cleaned_data['pfp']
            file_name = default_storage.save('profile_pictures/' + pfp_image.name, ContentFile(pfp_image.read()))
            user.userProfilePicture = file_name
        user.save()
        if 'delete_review' in request.POST:
            reviewId = request.POST['delete_review']
            review = Review.objects.filter(reviewId=reviewId, userReview=request.user).first()
            if review:
                review.delete()
        if 'username_color' in request.POST:
            color = request.POST['username_color']
            if color in ['black', '#03256C', '#FFF', '#2541B2']:
                request.session['username_color'] = color
        return redirect(reverse('view_profile'))
    return render(request, 'edit_profile.html', {'reviews': reviews, 'user': user, 'form': form})


def register(request):
    figures = Figure.objects.all()  
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
        
    return render(request, 'register.html', {'form': form, 'figures': figures})

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
        cityEvents = Event.objects.filter(eventLocation__iexact=city, eventDate=dateStripped, figureId__figureName__iexact=query, adminCheck=True)
        relatedFigures = Figure.objects.filter(event__in=cityEvents).distinct()
        relatedEvents = cityEvents
        searchedFigures = []  

    # Search Functionality: Handle City + Date 
    # - Display events only on the EXACT DATE INPUT + Related Figures for those exact events
    
    elif city and date:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        relatedEvents = Event.objects.filter(eventLocation__iexact=city, eventDate=dateStripped, adminCheck=True)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()

    # Search Functionality: Handle City + Keyword
    # - Display events ONLY related to the specific CITY and the Related Figures to these events.
    # - Empty Searched Figure to only show the related figures to the events.
    
    elif city and query:
        cityEvents = Event.objects.filter(eventLocation__iexact=city, figureId__figureName__iexact=query, adminCheck=True)
        relatedFigures = Figure.objects.filter(event__in=cityEvents).distinct()
        relatedEvents = cityEvents
        searchedFigures = []  
        
    # Search Functionality: Handle Date + Keyword
    # - Display events only on the EXACT DATE INPUT for the Figure Searched
    # - i.e User puts in 2024-05-30 "Drake", ONLY Drake Concerts show for this date
    # - Empty Searched Figure to only show specific EVENT for specific FIGURE

    elif date and query:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        relatedEvents = Event.objects.filter(eventDate=dateStripped, figureId__figureName__iexact=query, adminCheck=True)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()

    # Search Functionality: Handling Only City 
    # - Display events based on Event Location, Display Related Figures to these events.
    

    elif city:
        relatedEvents = Event.objects.filter(eventLocation__iexact=city, adminCheck=True)
        relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()

    # Search Functionality: Handling ONLY DATE 
    # - User searches by only date: Displays events on that date + Related Figures for the events 
    

    elif date:
        dateStripped = datetime.strptime(date, '%Y-%m-%d').date()
        relatedEvents = Event.objects.filter(eventDate=dateStripped, adminCheck=True)
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

        if query.lower() in genreMap:
            genreMap = genreMap[query.lower()]
            genreFigures = Figure.objects.filter(figureGenre__icontains=genreMap)
        else:
            genreFigures = Figure.objects.filter(figureGenre__icontains=query)

        if genreFigures.exists():
            relatedEvents = Event.objects.filter(figureId__in=genreFigures, adminCheck=True)
            relatedFigures = Figure.objects.filter(event__in=relatedEvents).distinct()
            searchedFigures = []

            return render(request, "search_results.html", {'searchedFigures': searchedFigures,
                                                        'relatedFigures': relatedFigures,
                                                        'relatedEvents': relatedEvents})
        else:
            searchedFigures = figures
            if exactFigures:
                initialFigure = exactFigures[0]
                relatedEvents = Event.objects.filter(figureId=initialFigure, adminCheck=True)
                relatedFigures = Figure.objects.filter(figureGenre=initialFigure.figureGenre).exclude(id=initialFigure.id)
                searchedFigures = exactFigures | partialFigures
            else:
                searchedFigures = figures.distinct()
                if searchedFigures.exists():
                    initialFigure = searchedFigures.first()
                    relatedFigures = Figure.objects.filter(figureGenre=initialFigure.figureGenre).exclude(id=initialFigure.id)
                    relatedEvents = Event.objects.filter(figureId=initialFigure, adminCheck=True)

    return render(request, "search_results.html", {'searchedFigures': searchedFigures, 
                                                            'relatedFigures': relatedFigures, 
                                                            'relatedEvents': relatedEvents})


def ticket_selection(request, eventid):
    tickets = Ticket.objects.filter(eventId=eventid).values()
    tickets_json = json.dumps(list(tickets))
    event = get_object_or_404(Event, pk=eventid)
    arena = Arena.objects.get(arenaName=event.arenaId)
    figure = Figure.objects.get(figureName=event.figureId)
    
    genre_map = {
        'Rock': 'concert',
        'Pop': 'concert',
        'Hip-Hop': 'concert',
        'R&B': 'concert',
        'Electronic': 'concert',
        'Jazz': 'concert',
        'Classical': 'concert',
        'Country': 'concert',
        'Blues': 'concert',
        'Reggae': 'concert',
        'Folk': 'concert',
        'Indie': 'concert',
        'Metal': 'concert',
        'Punk': 'concert',
    }
    
    sport_map = {
        'Hockey': 'sport',
        'Soccer': 'sport',
        'Basketball': 'sport',
        'Football': 'sport',
        'Tennis': 'sport',
        'Baseball': 'sport',
        'Golf': 'sport',
        'Cricket': 'sport',
        'Rugby': 'sport',
        'Volleyball': 'sport',
        'Boxing': 'sport',
        'MMA': 'sport',
        'Cycling': 'sport',
    }
    
    context = {
        'event' : event,
        'arena' : arena,
        'figure': figure,
        'tickets': tickets,
        'tickets_json' : tickets_json,
        'genre_map': genre_map
    }
    
    return render(request, "ticket_selection.html", context)


def temp(request):
    return render(request, "temp.html")

def checkout(request, event_id, selected_seats):
    selected_seat_nums = selected_seats.split(',')

    tickets = Ticket.objects.filter(eventId=event_id,seatNum__in=selected_seat_nums)
    


    return render(request, "checkout.html", {'event_id': event_id,'selected_seat_nums':selected_seat_nums ,'tickets': tickets})


# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
def payment(request):
    if request.method == "POST":
        
        
        selected_seats_str = request.POST.get('selected_seat_nums')
        selected_seats = json.loads(selected_seats_str.replace("'", "\""))
        event_id = request.POST.get('eventId')

        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('prov')
        payment_id = uuid.uuid4() 

        # Calculate total price for the selected tickets
        tickets = Ticket.objects.filter(eventId=event_id, seatNum__in=selected_seats)
        # if tickets.exists():
        #     response_data = {"success": True, "message": "Tickets exist."}
        # else:
        #     response_data = {"success": False, "message": "No tickets found."}

        # # Return JSON response
        # return JsonResponse(response_data)
        
           
        total_price = sum(ticket.ticketPrice for ticket in tickets)
        
        # Store payment details (without transactionId and paymentAmount as they'll be confirmed after payment)
        for ticket in tickets:
            Payment.objects.create(
                eventId=Event.objects.get(pk=event_id),
                seatNum=ticket,
                firstName=first_name,
                lastName=last_name,
                phoneNumber=phone_number,
                email=email,
                Address=address,
                city=city,
                province=province,
                paymentAmount=total_price,  # To be updated after payment confirmation
                paymentMethod="Stripe", # To be updated after payment confirmation
                
                paymentDate=datetime.now(),
                paymentId = payment_id
            )
        try:
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'cad',
                                'product_data': {
                                    'name': 'Event Tickets',
                                },
                                'unit_amount': (total_price*100) ,  # Stripe expects amount in cents
                            },
                            'quantity': 1,
                        },
                    ],
                    mode='payment',
                    success_url = request.build_absolute_uri(
                reverse('confirmation', kwargs={'paymentId': str(payment_id)})
            ),
                    cancel_url = request.build_absolute_uri('/'),
                )
                return redirect(checkout_session.url)
        except Exception as e:
                # Consider logging the error and returning an appropriate response
                return JsonResponse({'error': str(e)})

    # If not POST method, redirect to a relevant page or show an error
    return redirect('/error_page')




def filtered_events(request, eventGenre):
    filtered_events = Event.objects.filter(eventGenre=eventGenre)
    return render(request, 'filtered_events.html', {'filtered_events': filtered_events})

def figure(request, figure_name):
    figure_case = figure_name.lower()
    figure = get_object_or_404(Figure, figureName__iexact=figure_case)
    events = Event.objects.filter(figureId=figure, eventDate__gte=timezone.now(), adminCheck=True).order_by('eventDate', 'eventTime')
    
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
            review.userReview = request.user 
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

def confirmation(request,paymentId):

    payment = get_object_or_404(Payment, paymentId=paymentId)
    payment_id_reduced = str(payment.paymentId)[:4]
    
    transaction_id = f"{payment.eventId.pk}_{payment_id_reduced}"
    payment.transactionId = transaction_id
    payment.save()

    context = {}
    

    # payment = Payment.objects.filter(transactionId=transactionId)
    # ticket = Ticket.objects.filter(ticketId=ticketId).first()
    # user = payment.userId if payment else None
    # event = ticket.eventId if ticket else None
    # arena = ticket.arenaId if ticket else None

    context = {
        'payment': payment,
        # 'user': user,
        # 'ticket': ticket,
        # 'event': event,
        # 'arena': arena,
    }
    return render(request, "confirmation.html",context)
