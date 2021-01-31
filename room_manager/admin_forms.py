from django import forms
from .models import Building

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