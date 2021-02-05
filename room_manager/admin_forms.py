from django import forms
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
