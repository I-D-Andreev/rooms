from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.contrib.auth.models import User

from accounts.user_types import UserTypes
from .models import Meeting
from .room_manager import RoomManager

class BookRoomForm(forms.Form):
    date = forms.DateField(label="Date", widget=AdminDateWidget())
    time = forms.TimeField(label="Start Time", widget=AdminTimeWidget())
    duration = forms.IntegerField(min_value=0, label="Duration (min)", initial=0)
    participants_count = forms.IntegerField(min_value=0, label="Attendees", initial=0)


class DeleteMeetingForm(forms.ModelForm):
    meeting = forms.CharField()

    class Meta:
        model = Meeting
        fields = ['meeting', 'room', 'start_date', 'start_time', 'duration', 'participants_count']
        labels = {
            'room': 'Room',
            'start_date': 'Date',
            'start_time': 'Start Time',
            'duration': 'Duration (min)',
            'participants_count' : 'Attendees',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeleteMeetingForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['meeting'].widget = forms.Select(choices=self.__meeting_choice_list())
        self.fields['room'].widget = forms.TextInput() # remove drop-down menu

        for field in self.fields.items():
            if field[0] != 'meeting':
                field[1].disabled = True


    def __meeting_choice_list(self):
        meetings_list = []
        user_meetings = RoomManager.get_user_meetings_list(self.user)

        for meeting in user_meetings:
            meetings_list.append((meeting.id, str(meeting)))
        
        return meetings_list