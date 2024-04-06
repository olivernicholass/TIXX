from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Arena, Figure, Review, ReviewImage, User, Event

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstName = forms.CharField(max_length=30, required=False)
    lastName = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'userId', 'userPhoneNumber', 'userAddress', 'isOrganiser', 'firstName', 'lastName', 'favoriteFigure', 'stateProvince', 'postalcode', 'city')

    def __str__(self):
        return self.username
        
class CreateEventForm(forms.ModelForm):
    arenaId = forms.ModelChoiceField(queryset=Arena.objects.all(), label='Arena')
    figureId = forms.ModelChoiceField(queryset=Figure.objects.all(), label='Figure')

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
        self.fields['reviewImage'].required = False\
            
class EditProfileForm(forms.Form):
    firstName = forms.CharField(max_length=50, required=False)
    lastName = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    userPhoneNumber = forms.CharField(max_length=20, required=False)
    userAddress = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    stateProvince = forms.CharField(max_length=100, required=False)
    postalcode = forms.CharField(max_length=20, required=False)
    favoriteSongSpotifyId = forms.CharField(max_length=255, required=False)
    userDescription = forms.CharField(max_length=255, required=False)
    mini_image = forms.ImageField(required=False)
    pfp = forms.ImageField(required=False)

    def clean_favoriteSongSpotifyId(self):
        data = self.cleaned_data['favoriteSongSpotifyId']
        if data:
            if len(data) != 22:
                raise forms.ValidationError('Spotify ID should be 22 characters long.')
        return data

    def clean_userDescription(self):
        data = self.cleaned_data['userDescription']
        if data:
            if len(data) > 200:
                raise forms.ValidationError('Description should be at most 200 characters long.')
        return data

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
    
