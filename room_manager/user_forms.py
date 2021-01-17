from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

class BookRoomForm(forms.Form):
    date = forms.DateField(label="Date", widget=AdminDateWidget())
    time = forms.TimeField(label="Start Time", widget=AdminTimeWidget())
    duration = forms.IntegerField(min_value=0, label="Duration (min)", initial=0)
    participants_count = forms.IntegerField(min_value=0, label="Attendees", initial=0)

