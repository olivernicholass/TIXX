from django.shortcuts import render, HttpResponse


# Create your views here.

def home(request):
    return render(request, "home.html")

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

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

def filtered_events(request):
    return render(request, "filtered_events.html")

def figure(request):
    return render(request, "figure.html")
