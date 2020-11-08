from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def login_view(request, *args, **kwargs):
    form = AuthenticationForm()
    args = {'form': form}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/manager/dashboard')
        else:
            messages.error(request, 'Incorrect username or password!')

    return render(request, 'accounts/login.html', args)


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
