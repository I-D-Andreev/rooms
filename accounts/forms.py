from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group

User = get_user_model()

def get_user_group_choices():
    group_choices = []
    groups = Group.objects.all()
    
    for group in groups:
        group_choices.append((group, group))

    return group_choices

class UserRegistrationForm(UserCreationForm):
    group = forms.CharField(widget=forms.Select(choices=get_user_group_choices()))

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
