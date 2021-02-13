from django import forms
from .meeting_distance_types import MeetingDistanceTypes
from .models import SystemConstants
from .location_models import Building

class CreateBuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'description']
        labels = {
            'name': 'Building Name',
            'description': 'Description (optional)'
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'style': 'resize:none'})
        }


# Bind a Select element to display all the floors of a building
class ChooseBuildingForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='')


class MeetingRoomDistanceForm(forms.Form):
    type = forms.CharField(widget=forms.Select(choices=MeetingDistanceTypes.as_choice_list()),initial=SystemConstants.get_constants().distance_type)
    floors = forms.IntegerField(min_value=0, initial=SystemConstants.get_constants().distance_floors, required=False)