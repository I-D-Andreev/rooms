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
    type = forms.CharField(widget=forms.Select(choices=MeetingDistanceTypes.as_choice_list()))
    floors = forms.IntegerField(min_value=0, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        constants = SystemConstants.get_constants()
        self.fields['type'].initial = constants.distance_type
        self.fields['floors'].initial = constants.distance_floors


    def update_data(self):
        if self.is_valid():
            try:
                cleaned_type = self.cleaned_data['type']
                cleaned_floors = int(self.cleaned_data['floors'])
                
                SystemConstants.update_meeting_room_distance_constants(cleaned_type, cleaned_floors) 
                return True
            except Exception as e:
                print(e)

        return False