from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('events/', views.events, name='events'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
     path('search/', views.search_results, name='search_results'),
    path('tickets/', views.ticket_selection, name='ticket_selection'),
    path('checkout/', views.checkout, name='checkout'),
    path('filtered_events/<slug:eventGenre>/', views.filtered_events, name='filtered_events'),
    path('figure/', views.figure, name='figure'),
    path('get-ticket-data/', views.get_ticket_data, name='get_ticket_data'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

