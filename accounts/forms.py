from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group
from django.shortcuts import HttpResponse
from accounts.user_groups import UserGroups

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
        group_name = self.cleaned_data['group']
        user_group = None
        try:
            user_group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            user_group = Group.objects.get(name=UserGroups.users)

        user = super(UserCreationForm, self).save(commit)
        user_group.user_set.add(user)

        return user
