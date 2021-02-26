from django.contrib import messages
from .user_forms import BookRoomForm, DeleteMeetingForm, ChooseRoomForm
from .room_manager import RoomManager
from django.shortcuts import render
from .models import Meeting
from .room_forms import BookNowForm
from accounts.models import Profile
from .forms import AccountInfoForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from room_manager.decorators import user_only


# login + user only
def book_room_view(request, *args, **kwargs):
    form = BookRoomForm()

    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            meeting_name = cleaned_data['name']
            participants = cleaned_data['participants_count']
            date = cleaned_data['date']
            time = cleaned_data['time']
            duration = cleaned_data['duration']

            meeting, err_text = RoomManager.schedule_meeting(meeting_name, participants, date, time, duration, request.user)

            if meeting is None:
                messages.error(request, err_text)
            else:
                messages.success(request, f"Successfully booked room \"{meeting.room.public_name}\" from {meeting.start_time_str()} to {meeting.end_time_str()}.")
                form = BookRoomForm()


    context = {'form': form}
    return render(request, 'room_manager/user/book_room.html', context)


# login + user only
def cancel_booking_view(request, *args, **kwargs):

    if request.method == 'POST':
        meeting_id = request.POST['meeting']
        meeting = Meeting.objects.filter(pk=meeting_id).first()
        
        failed_cancel = True
        if meeting is not None:
            resp = meeting.delete()
            if resp[0] >= 1:
                failed_cancel = False
        
        if failed_cancel:
            messages.error(request, 'Failed to cancel the booking!')
        else:
            messages.success(request, f'The booking has been successfully cancelled!\n {meeting.long_name()}')

    form = DeleteMeetingForm(user=request.user)
    context  = {'form': form}
    return render(request, 'room_manager/user/cancel_booking.html', context)

# login + user only
def my_schedule_view(request, *args, **kwargs):
    meetings_list = RoomManager.get_user_meetings_list_from_now(request.user)
    context = {'meetings_list' : meetings_list}
    return render(request, 'room_manager/user/my_schedule.html', context)

# login + user only
def room_schedule_view(request, *args, **kwargs):
    form = ChooseRoomForm()
    context = {'form': form}
    return render(request, 'room_manager/user/room_schedule.html', context)

# login + room only
def book_now_view(request, *args, **kwargs):
    profile_id = request.POST.get('id', None) if request.method == "POST" else request.GET.get('id', None)
    profile = None if not profile_id else Profile.objects.filter(pk=profile_id).first()


    if request.method == 'POST':
        form = BookNowForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            meeting_name = cleaned_data['meeting_name']
            duration = cleaned_data['duration']

            # If valid id is passed, book the room with specified id, else book current room.
            room_to_book = request.user
            if profile:
                room_to_book = profile.user

            meeting = RoomManager.try_book_room_now(room_to_book, meeting_name, duration)

            if meeting is not None:
                messages.success(request, f"Room {room_to_book.profile.public_name} booked successfully!")
            else:
                messages.error(request, "Booking failed!")

    form = BookNowForm()
         
    context = {'form': form, 'profile': profile}
    return render(request, 'room_manager/room/book_now.html', context)


# login + (user or admin)
def edit_account_view(request, *args, **kwargs):

    info_form = AccountInfoForm(user=request.user)
    sensitive_info_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if request.POST.__contains__('public_name') or request.POST.__contains__('email'):
            info_form = AccountInfoForm(request.POST, user=request.user)
            if info_form.is_valid():
                if info_form.update_fields():
                    messages.success(request, "Successfully updated your information!", extra_tags="account_info")
                else:
                    messages.error(request, "An error occurred while updating your information!", extra_tags="account_info")
        
        elif request.POST.__contains__('old_password') or request.POST.__contains__('new_password'):
            sensitive_info_form = PasswordChangeForm(data=request.POST, user=request.user)

            if sensitive_info_form.is_valid():
                sensitive_info_form.save()
                update_session_auth_hash(request, sensitive_info_form.user)
                messages.success(request, "Password successfully changed!", extra_tags="sensitive_info")
            else:
                messages.error(request, "Failed to change password!", extra_tags="sensitive_info")
            
    context = {'info_form': info_form, 'sensitive_info_form': sensitive_info_form}
    return render(request, 'room_manager/edit_account.html', context)


