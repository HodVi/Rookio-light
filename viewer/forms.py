from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from viewer.models import Room, Tag, MenuItem


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
                  'minimum_participants',
                  'maximum_participants'
                  ]


class TagForm(forms.Form):
    name = forms.CharField(max_length=25, label='Tags')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError("Tag name cannot be empty.")
        # this part is no longer needed because we WANT an existing tag to be assigned to a newly created room
        # if Tag.objects.filter(name=name).exists():
        #     raise ValidationError("Tag with this name already exists.")
        return name


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['item_name', 'price', 'duration', 'number_of_pieces']

        widgets = {
            'item_name':
                forms.TextInput(attrs={'class': 'bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full '
                                                'py-2 px-4 text-gray-700 leading-tight focus:outline-none '
                                                'focus:bg-white focus:border-blue-500'
                                       }
                                ),
            'price':
                forms.NumberInput(attrs={'class': 'bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full '
                                                  'py-2 px-4 text-gray-700 leading-tight focus:outline-none '
                                                  'focus:bg-white focus:border-blue-500'
                                         }
                                  ),
            'duration':
                forms.NumberInput(attrs={'class': 'bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full '
                                                  'py-2 px-4 text-gray-700 leading-tight focus:outline-none '
                                                  'focus:bg-white focus:border-blue-500'
                                         }
                                  ),
            'number_of_pieces':
                forms.NumberInput(attrs={'class': 'bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full '
                                                  'py-2 px-4 text-gray-700 leading-tight focus:outline-none '
                                                  'focus:bg-white focus:border-blue-500'
                                         }
                                  ),
        }