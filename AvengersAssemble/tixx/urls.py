from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
     path('search/', views.search_results, name='search_results'),
    path('tickets/', views.ticket_selection, name='ticket_selection'),
    path('checkout/', views.checkout, name='checkout'),
    path('filtered_events/<slug:eventGenre>/', views.filtered_events, name='filtered_events'),
    path('figure/', views.figure, name='figure'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

