from django.contrib.auth import authenticate
from room_manager.room_manager import RoomManager
from django import forms
from django.db import transaction

from .location_models import Floor, Building
from .models import Meeting
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
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}), required=False)

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

    def try_cancel_meeting(self):
        if self.is_valid():
            cleaned_data = self.cleaned_data
            
            meeting_id = cleaned_data['meeting']
            password = cleaned_data['password']

            meeting = Meeting.objects.filter(pk=meeting_id).first()
            if meeting:
                
                # Instant-bookings to be canceled by everyone
                if meeting.creator.type == UserTypes.room:
                    return self.__try_delete_meeting(meeting)

                username = meeting.creator.user.username
                user = authenticate(username=username, password=password)

                if user and user.id == meeting.creator.user.id:
                    return self.__try_delete_meeting(meeting)

        return False



    def __try_delete_meeting(self, meeting: Meeting):
        resp = meeting.delete()
        if resp[0] >= 1:
            return True
        
        return False

class RoomLogoutForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(RoomLogoutForm, self).__init__(*args, **kwargs)

        self.room = user
    
    def try_logout(self):
        if self.is_valid():
            cleaned_data = self.cleaned_data

            username = cleaned_data['username']
            password  = cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                if user.profile.type == UserTypes.admin or user.id == self.room.id:
                    return True

        return False


class DeleteRoomForm(forms.Form):
    room = forms.ModelChoiceField(queryset=Profile.objects.filter(type__exact=UserTypes.room), empty_label="", label="Choose a Room")
    
    # These fields are used just to display the information
    username = forms.CharField(required=False, label='Room Account Username')
    public_name = forms.CharField(required=False, label='Room Name')
    email = forms.CharField(required=False, label='Room Email')
    capacity = forms.CharField(required=False)
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='All Buildings', label='Building', required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='', label='Location', required=False)


    def delete_room(self):
        if self.is_valid():
            try:
                room = self.cleaned_data["room"]

                meetings_ongoing_or_in_future = room.meetings_ongoing_or_in_future()

                if len(meetings_ongoing_or_in_future) > 0:
                    users_who_booked_meetings = set([meeting.creator.public_name for meeting in meetings_ongoing_or_in_future])
                    error_msg = "Rooms with ongoing meetings or with meetings booked in the future can not be deleted! \
                        The following users have currently booked a meeting in this room: " \
                        + (", ".join(users_who_booked_meetings)) + "."

                    return False, error_msg
                
                room.user.delete()
                return True, "Room successfully deleted!"
            except Exception as e:
                print(e)

        return False, "Failed to delete room!"