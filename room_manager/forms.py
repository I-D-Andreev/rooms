from django import forms
from django.db import transaction

from .location_models import Floor, Building

class AccountInfoForm(forms.Form):
    public_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='All Buildings', label='Building', required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='', label='Location', required=False)
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AccountInfoForm, self).__init__(*args, **kwargs)
        self.user = user

        self.initial_email = self.user.email
        self.initial_public_name = self.user.profile.public_name
        self.initial_floor = self.user.profile.floor
        self.initial_building = self.initial_floor.building if self.initial_floor else None

        self.fields['email'].initial = self.initial_email
        self.fields['public_name'].initial = self.initial_public_name
        self.fields['floor'].initial = self.initial_floor


    def update_fields(self):
        if self.is_valid():
            try:
                self.user.email = self.cleaned_data['email']
                self.user.profile.public_name = self.cleaned_data['public_name']
                self.user.profile.floor = self.cleaned_data['floor']

                with transaction.atomic():
                    self.user.save()
                    self.user.profile.save()

                return True
            except:
                return False

        return False
