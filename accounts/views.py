from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from room_manager.views import dashboard_view


def login_view(request, *args, **kwargs):
    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(dashboard_view)
        else:
            messages.error(request, 'Incorrect username or password!')
    
    args = {'form': form}
    return render(request, 'accounts/login.html', args)

def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect(login_view)


def register_view(request, *args, **kwargs):

    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(dashboard_view)
   
    args = {'form': form}
    return render(request, 'accounts/register.html', args)
