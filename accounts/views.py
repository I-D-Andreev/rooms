from accounts.models import RegistrationLink, ForgottenPasswordLink
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib import messages
from room_manager.views import dashboard_view
from accounts.decorators import unauthenticated_user_only
from django.contrib.auth.decorators import login_required
from .user_types import UserTypes
from room_manager.room_forms import RoomLogoutForm


@unauthenticated_user_only
def login_view(request, *args, **kwargs):
    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if (user is not None) and (hasattr(user, 'profile')):
            login(request, user)
            return redirect(dashboard_view)
        else:
            messages.error(request, 'Incorrect username or password!')

    args = {'form': form}
    return render(request, 'accounts/login.html', args)


# No need for decorator as the page just redirects.
def logout_view(request, *args, **kwargs):
    if hasattr(request.user, 'profile') and request.user.profile.type == UserTypes.room:
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


# No need for decorator, as we do our own filtering.
def register_view(request, code, *args, **kwargs):
    reg_link = RegistrationLink.get_all_valid_links().filter(unique_code__exact=code).first()

    if not reg_link:
        return render(request, 'accounts/register_invalid.html')

    form = UserRegistrationForm()

    if request.method == 'POST':
        edited_request = request.POST.copy()
        edited_request.update({'type': reg_link.type, 'capacity': 0})

        form = UserRegistrationForm(edited_request)

        if form.is_valid():
            user = form.save()

            if user:
                reg_link.delete()
                login(request, user)
                return redirect(dashboard_view)
            else:
                messages.error(request, "Failed to create account!")
    
    args = {'form': form, 'acc_type': str(reg_link.type).capitalize()}
    return render(request, 'accounts/register.html', args)


# No need for decorator, as we do our own filtering.
def password_reset_view(request, code, *args, **kwargs):
    reset_link = ForgottenPasswordLink.get_all_valid_links().filter(unique_code__exact=code).first()

    if not reset_link:
        return render(request, 'accounts/password_reset_invalid.html')

    form = SetPasswordForm(reset_link.profile.user)
    
    if request.method == 'POST':
        form = SetPasswordForm(user=reset_link.profile.user, data=request.POST)

        if form.is_valid():
            form.save()
            reset_link.delete()
            return redirect(dashboard_view)
        else:
            messages.error(request, "Failed to update password.")


    context = {'form': form}
    return render(request, 'accounts/password_reset.html', context)
