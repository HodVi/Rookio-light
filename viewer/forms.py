from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from viewer.models import Room


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=64, required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name',
                  'room_type',
                  'description',
                  'place',
                  'gps_description',
                  'gps_lat',
                  'gps_lng',
                  'date',
                  'time',
                  'outdoor',
                  'contact_public',
                  'contact_after_assignment',
                  'age_restriction',
                  'age_recommendation',
                  'minimum_participants'
                  # 'maximum_participants'
                  ]
