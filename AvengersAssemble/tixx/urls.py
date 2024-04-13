from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/', views.register, name='register'),
    path('search/', views.search_results, name='search_results'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),    
    path('edit/profile/', views.edit_profile, name='edit_profile'), 
    path('register/', views.register, name='register'),
    path('search_results/', views.search_results, name='search_results'),
    path('tickets/<str:eventid>/', views.ticket_selection, name='ticket_selection'),
    path('checkout/<int:event_id>/<str:selected_seats>/', views.checkout, name='checkout'),
    path('review/<str:figure_name>/', views.review, name='review'),
    path('filtered_events/<slug:eventGenre>/', views.filtered_events, name='filtered_events'),
    path('figure/<str:figure_name>/', views.figure, name='figure'),
    path('organiser/create_event/', views.create_event, name='create_event'),
    path('confirmation/<uuid:paymentId>/', views.confirmation, name='confirmation'),
    path('organiser/login/', views.organiser_login, name='organiser_login'),
    path('organiser/register/', views.organiser_register, name='organiser_register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin_review/', views.admin_review, name='admin_review'),
    path('organiser/dashboard/', views.dashboard_home, name='dashboard_home'),
    path('organiser/dashboard/statistics/', views.dashboard_statistics, name='dashboard_statistics'),
    path('organiser/dashboard/edit/<int:event_id>', views.edit_event, name='edit_event'),
    path('organiser/dashboard/delete/<int:event_id>', views.delete_event, name='delete_event'),
    path('organiser/dashboard/events/<int:event_id>/', views.event_overview, name='event_overview'), 
    path('payment/', views.payment, name='payment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

