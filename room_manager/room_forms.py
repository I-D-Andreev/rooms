from django import forms

class BookNowForm(forms.Form):
    meeting_name = forms.CharField(initial="Instant Booking", label="Meeting Name")
    duration = forms.IntegerField(min_value=0, label="Duration (min)", widget=forms.NumberInput(attrs={'autofocus': 'autofocus'}))