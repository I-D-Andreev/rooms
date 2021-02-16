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
    infer_nearby_buildings = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        constants = SystemConstants.get_constants()
        self.fields['type'].initial = constants.distance_type
        self.fields['floors'].initial = constants.distance_floors
        self.fields['infer_nearby_buildings'].initial = constants.infer_nearby_buildings


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


class NearbyBuildingsForm(forms.Form):
    building1 = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='', required=True)
    building2 = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='', required=True)

    def add_near_buildings_pair(self):
        if self.is_valid():
            try:
                building1 = self.cleaned_data['building1']
                building2 = self.cleaned_data['building2']
                
                if building1.id == building2.id:
                    return False, "A building can't be paired with itself!"


                if (building1 in building2.close_buildings.all()) or \
                    (building2 in building1.close_buildings.all()):
                    return False, f'Building pair "{building1.name} - {building2.name}" already exists!'
                
                building1.close_buildings.add(building2)

                return True, 'Successfully added the building pair!'
            except Exception as e:
                print(e)
        
        return False, 'Failed to add the building pair!'