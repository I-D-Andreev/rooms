from django.forms.widgets import PasswordInput
from room_manager.room_manager import RoomManager
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


class CancelMeetingForm(forms.Form):
    meeting = forms.CharField(widget=None, label='Choose a Meeting')
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CancelMeetingForm, self).__init__(*args, **kwargs)
    
        self.room = user

        choices_list = [('', '')] + self.__meeting_choice_list()
        self.fields['meeting'].widget = forms.Select(choices=choices_list)
        
        # Will be populated by us with the meeting creator's name
        self.fields['username'].disabled = True


    def __meeting_choice_list(self):
        meetings = RoomManager.get_room_meetings_list_from_now(self.room)
        return [(meeting.id, str(meeting)) for meeting in meetings]

