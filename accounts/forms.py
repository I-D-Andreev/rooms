from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import transaction


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
        if self.is_valid():
            cleaned_type = self.cleaned_data['type']
            cleaned_capacity = self.cleaned_data.get('capacity')

            account_type = cleaned_type if cleaned_type in UserTypes.as_list() else UserTypes.user

            user = super(UserCreationForm, self).save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                try:
                    with transaction.atomic():
                        user.save()
                        Profile.objects.create(user=user, public_name=user.username, type=account_type, capacity=cleaned_capacity)
                
                except Exception as e:
                    print(f"Error: {e}")
                    return None

            return user
        else:
            return None
