from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Review, ReviewImage, User, Event

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstName = forms.CharField(max_length=30, required=False)
    lastName = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'userId', 'userPhoneNumber', 'userAddress', 'isOrganiser', 'firstName', 'lastName')

    def __str__(self):
        return self.username
        
class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['eventName', 'eventDate', 'eventTime', 'eventLocation', 'eventDescription', 'eventStatus', 'eventGenre', 'eventImage', 'arenaId', 'figureId']
    

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
        
class OrganiserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    isOrganiser = forms.BooleanField(initial=True, required=False)
    organiserCredentials = forms.CharField(max_length=100, required=False)
    userPhoneNumber = forms.CharField(max_length=10) 
    userAddress = forms.CharField(max_length=100)
    secretKeyword = "tixxEVENTORGANISER"  

    class Meta:
        model = User
        fields = ['username', 'password', 'isOrganiser', 'organiserCredentials', 'email', 'userPhoneNumber', 'userAddress']

    def clean_organiserCredentials(self):
        organiserCredentials = self.cleaned_data.get('organiserCredentials')
        if organiserCredentials != self.secretKeyword:
            raise forms.ValidationError("Invalid secret keyword. Contact tixxEVENTS@gmail.com to request a secret key.")
        return organiserCredentials
    
