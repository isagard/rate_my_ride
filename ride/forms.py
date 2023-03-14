from django import forms
from ride.models import Review, ServicePage
from django.contrib.auth.models import User
from ride.models import UserProfile

class ReviewForm(forms.ModelForm):
    
    ratingChoices = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]

    title = forms.CharField(max_length=128, help_text="Please enter a title for your review.")
    rating = forms.ChoiceField(choices=ratingChoices, widget=forms.RadioSelect, help_text="Please select a rating.")
    location = forms.CharField(max_length=32, help_text="Please enter the city you took the taxi from for your review.")
    body = forms.CharField(max_length=256, help_text="Please talk about your experience.")
    service = forms.CharField(max_length=32, help_text="Please enter the name of the taxi service for your review.")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Review
        fields = ('title', 'rating', 'location', 'body', 'service')

class ServiceForm(forms.ModelForm):

    name = forms.CharField(max_length=32, help_text="Please enter your service name.")
    location = forms.CharField(max_length=32, help_text="Please enter your service location.")
    body = forms.CharField(max_length=256, help_text="Please enter a description of your service.")
    logo = forms.ImageField(label='Upload your logo')

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = ServicePage
        fields = ('name', 'location', 'body', 'logo')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('accountUser', 'picture',)