from django import forms
from django.db import transaction

from .location_models import Floor, Building
from accounts.models import Profile
from accounts.user_types import UserTypes


class BookNowForm(forms.Form):
    meeting_name = forms.CharField(initial="Instant Booking", label="Meeting Name")
    duration = forms.IntegerField(min_value=0, label="Duration (min)", widget=forms.NumberInput(attrs={'autofocus': 'autofocus'}))


class EditRoomForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Profile.objects.filter(type__exact=UserTypes.room), empty_label="", label="Choose Room")
    public_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    capacity = forms.IntegerField()

    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='All Buildings', label='Building', required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='', label='Location', required=False)

    def update_fields(self):
        if self.is_valid():
            try:
                cleaned_data = self.cleaned_data
                profile = cleaned_data['room']
                profile.public_name = cleaned_data['public_name']
                profile.user.email = cleaned_data['email']
                profile.capacity = cleaned_data['capacity']
                profile.floor = cleaned_data['floor']

                with transaction.atomic():
                    profile.save()
                    profile.user.save()

                return True
            except Exception as ex:
                print(ex)

        return False