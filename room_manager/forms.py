from django import forms
from django.db import transaction

class AccountInfoForm(forms.Form):
    public_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AccountInfoForm, self).__init__(*args, **kwargs)
        self.user = user

        self.initial_email = self.user.email
        self.initial_public_name = self.user.profile.public_name

        self.fields['email'].initial = self.initial_email
        self.fields['public_name'].initial = self.initial_public_name


    def update_fields(self):
        if self.is_valid():
            try:
                self.user.email = self.cleaned_data['email']
                self.user.profile.public_name = self.cleaned_data['public_name']

                with transaction.atomic():
                    self.user.save()
                    self.user.profile.save()

                return True
            except:
                return False

        return False


class AccountSensitiveInfoForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['old_password', 'new_password1' ,'new_password2']
        labels = {
            'old_password': 'Old Password',
            'new_password1': 'New Password',
            'new_password2': 'Repeat New Password',
        }
