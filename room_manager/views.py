from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from room_manager.decorators import user_only
from accounts.forms import UserRegistrationForm
from accounts.user_types import UserTypes
from django.contrib import messages
from .user_forms import BookRoomForm
from .room_manager import RoomManager



@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    try:
        dashboard = request.user.profile.type
    except ObjectDoesNotExist:
        raise PermissionDenied()

    args = {'username': request.user.username}
    return render(request, f'room_manager/{dashboard}_dashboard.html', args)


@login_required(login_url='login')
@user_only
def statistics_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/statistics.html')


# login + admin only
def create_room_view(request, *args, **kwargs):
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        edited_request = request.POST.copy()
        edited_request.update({'type': UserTypes.room})

        form = UserRegistrationForm(edited_request)

        if form.is_valid():
            print("form is valid")
            form.save()
            messages.info(request, f"Room {form.cleaned_data['username']} created successfully!")

            # clean the form
            form = UserRegistrationForm()
        else:
            print('form is not valid')
            print(form.errors)

    args = {'form': form}
    return render(request, 'room_manager/admin/create_room.html', args)


# login + user only
def book_room_view(request, *args, **kwargs):
    form = BookRoomForm()

    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            participants = cleaned_data['participants_count']
            date = cleaned_data['date']
            time = cleaned_data['time']
            duration = cleaned_data['duration']
            
            room_manager = RoomManager(participants, date, time, duration)
            room_manager.print()
            room_manager.print_range()



            print('Form is valid')
        else:
            print('Form is not valid')

    args = {'form': form}
    return render(request, 'room_manager/user/book_room.html', args)