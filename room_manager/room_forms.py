from django import forms

from .location_models import Floor, Building

class BookNowForm(forms.Form):
    meeting_name = forms.CharField(initial="Instant Booking", label="Meeting Name")
    duration = forms.IntegerField(min_value=0, label="Duration (min)", widget=forms.NumberInput(attrs={'autofocus': 'autofocus'}))


class EditRoomForm(forms.Form):
    public_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    capacity = forms.IntegerField()

    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='All Buildings', label='Building', required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='', label='Location')
