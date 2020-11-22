from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

FRUIT_CHOICES= [
    ('orange', 'Oranges'),
    ('cantaloupe', 'Cantaloupes'),
    ('mango', 'Mangoes'),
    ('honeydew', 'Honeydews'),
    ]


class UserRegistrationForm(UserCreationForm):
    group = forms.CharField(widget=forms.Select(choices=FRUIT_CHOICES))


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


    def save(self, commit=True):
        print(f'Group is : {self.cleaned_data["group"]}')
        user = super(UserCreationForm, self).save(commit)
        #  add to group
        return user
