from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


def register_view(request, *args, **kwargs):

    form = UserRegistrationForm()
    args = {'form': form}

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/manager/dashboard')

    return render(request, 'accounts/register.html', args)
