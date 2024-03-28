from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('search_results/', views.search_results, name='search_results'),
    path('tickets/<str:eventid>/', views.ticket_selection, name='ticket_selection'),
    path('checkout/', views.checkout, name='checkout'),
    path('review/<str:figure_name>/', views.review, name='review'),
    path('filtered_events/<slug:eventGenre>/', views.filtered_events, name='filtered_events'),
    path('figure/<str:figure_name>/', views.figure, name='figure'),
    path('guest_organiser/', views.guest_organiser, name='guest_organiser'),
    path('temp/', views.temp, name='temp'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('organiser_login/', views.organiser_login, name='organiser_login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

