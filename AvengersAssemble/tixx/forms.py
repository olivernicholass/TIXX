from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, ReviewImage


class RegisterForm(UnboundLocalError):
      username = forms.CharField(widget=forms.TextInput)
      email = forms.EmailField(widget=forms.EmailInput)
      password1 = forms.CharField(widget=forms.PasswordInput)
      password2 = forms.CharField(widget=forms.PasswordInput)

      class Meta:
            model = User
            fields = ["username", "email", "password1", "password2"]


class GuestOrganiserForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=100, required=True)
    number_of_tickets = forms.IntegerField(label='Number of Tickets', required=True)
    event_location = forms.CharField(label='Event Location', max_length=100, required=True)
    ticket_price = forms.DecimalField(label='Ticket Price', max_digits=8, decimal_places=2, required=True)
    date_of_event = forms.DateField(label='Date of Event', required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    venue_name = forms.CharField(label='Venue Name', max_length=100, required=True)
    genre = forms.CharField(label='Genre', max_length=100, required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=True)
    

class ReviewForm(forms.ModelForm):
    reviewImage = forms.ImageField(widget=forms.FileInput(attrs={'accept': 'image/*', 'placeholder': 'Upload image'}))

    class Meta:
        model = Review
        fields = ['reviewRating', 'reviewTitle', 'reviewText', 'reviewDate', 'reviewImage']
        widgets = {
            'reviewTitle': forms.TextInput(attrs={'placeholder': 'Enter review title'}),
            'reviewText': forms.Textarea(attrs={'placeholder': 'A brief summary of your experience.'}),
            'reviewDate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reviewImage'].required = False

class ReviewImageForm(forms.ModelForm):
    class Meta:
        model = ReviewImage
        fields = ['reviewImage']
        widgets = {
            'reviewImage': forms.FileInput(attrs={'accept': 'image/*', 'placeholder': 'Upload image'}),
        }