# all form classes

from django import forms

class GuestOrganiserForm(forms.Form):
    company_name = forms.CharField(label='Company Name', max_length=100, required=True)
    number_of_tickets = forms.IntegerField(label='Number of Tickets', required=True)
    event_location = forms.CharField(label='Event Location', max_length=100, required=True)
    ticket_price = forms.DecimalField(label='Ticket Price', max_digits=8, decimal_places=2, required=True)
    date_of_event = forms.DateField(label='Date of Event', required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    venue_name = forms.CharField(label='Venue Name', max_length=100, required=True)
    genre = forms.CharField(label='Genre', max_length=100, required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=True)
