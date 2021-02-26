from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from room_manager.views import dashboard_view
from accounts.decorators import unauthenticated_user_only
from django.contrib.auth.decorators import login_required
from .user_types import UserTypes
from room_manager.room_forms import RoomLogoutForm


# @unauthenticated_user_only
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


@login_required(login_url='login')
def logout_view(request, *args, **kwargs):
    if request.user.profile.type == UserTypes.room:
        form = RoomLogoutForm(user=request.user)

        if request.method == "POST": 
            form = RoomLogoutForm(request.POST, user=request.user)

            if form.is_valid():
                if form.try_logout():
                    logout(request)
                    return redirect(login_view)
            
            messages.error(request, "Logout failed!")

        context = {'form': form}
        return render(request, 'accounts/room_logout.html', context)

    logout(request)
    return redirect(login_view)


# @unauthenticated_user_only
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
