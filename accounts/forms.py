from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from accounts.user_types import UserTypes
from accounts.models import Profile


class UserRegistrationForm(UserCreationForm):
    capacity = forms.IntegerField(min_value=0)
    type = forms.CharField(widget=forms.Select(choices=UserTypes.as_choice_list()))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit=True):
        cleaned_type = self.cleaned_data['type']
        cleaned_capacity = self.cleaned_data.get('capacity', 0)

        account_type = cleaned_type if cleaned_type in UserTypes.as_list() else UserTypes.as_list()[1]

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Profile.objects.create(user=user, public_name=user.username, type=account_type, capacity=cleaned_capacity)


        return user
