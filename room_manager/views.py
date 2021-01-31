from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from room_manager.decorators import user_only
from accounts.forms import UserRegistrationForm
from accounts.user_types import UserTypes
from django.contrib import messages
from .user_forms import BookRoomForm, DeleteMeetingForm, ChooseRoomForm
from .room_manager import RoomManager
from django.http import JsonResponse
from .models import Meeting
from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import Profile
from django.http import HttpResponse
from .forms import AccountInfoForm
from .admin_forms import CreateBuildingForm, ChooseBuildingForm
from .room_forms import BookNowForm
import json

# --------------- Views ---------------
@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    try:
        dashboard = request.user.profile.type
    except ObjectDoesNotExist:
        raise PermissionDenied()

    
    meetings_list = None
    if request.user.profile.type == UserTypes.user:
        meetings_list = RoomManager.get_user_meetings_list_today(request.user)
    elif request.user.profile.type == UserTypes.room:
      meetings_list = get_room_schedule_meetings_list(request.user)


    context = {'user': request.user, 'meetings_list': meetings_list}

    return render(request, f'room_manager/{dashboard}_dashboard.html', context)

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

# @login_required(login_url='login')
# @user_only
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
            form.save()
            messages.success(request, f"Room \"{form.cleaned_data['username']}\" created successfully!")

            # clean the form
            form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'room_manager/admin/create_room.html', context)


# login + admin only
def create_building_view(request, *args, **kwargs):
    form = CreateBuildingForm()

    if request.method == 'POST':
        form = CreateBuildingForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Building \"{form.cleaned_data['name']}\" createad successfully!")

            # clean the form
            form = CreateBuildingForm()


    context = {'form': form}
    return render(request, 'room_manager/admin/create_building.html', context)


# login + admin only
def configure_floors_view(request, *args, **kwargs):
    form = ChooseBuildingForm()
    context = {'form': form}
    return render(request, 'room_manager/admin/configure_floors.html', context)

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

            meeting = RoomManager.schedule_meeting(meeting_name, participants, date, time, duration, request.user)

            if meeting is None:
                messages.error(request, 'There is no free room for the chosen time!')
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

# login + user only
def multi_room_schedule_view(request, *args, **kwargs):
    rooms = Profile.objects.filter(type__exact = UserTypes.room)
    multi_room_schedule_list = [(room, get_room_schedule_meetings_list(room.user)) for room in rooms]
    context = {'list': multi_room_schedule_list}
    return render(request, 'room_manager/user/multi_room_schedule.html', context)


# login + room only
def book_now_view(request, *args, **kwargs):
    form = BookNowForm()

    if request.method == 'POST':
        form = BookNowForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            meeting_name = cleaned_data['meeting_name']
            duration = cleaned_data['duration']

            meeting = RoomManager.try_book_room_now(request.user, meeting_name, duration)

            if meeting is not None:
                return redirect(dashboard_view, *args, **kwargs)

        
        messages.error(request, "Booking failed!")
    
    context = {'form': form}
    return render(request, 'room_manager/room/book_now.html', context)

# --------------- REST API ---------------

def get_meeting(request, id, *args, **kwargs):
    meeting = Meeting.objects.filter(pk=id).first()

    if meeting is not None:
        return JsonResponse({
            'id' : meeting.pk,
            'room' : meeting.room.public_name,
            'start_date' : meeting.start_date,
            'start_time' : meeting.start_time,
            'duration': meeting.duration,
            'participants_count': meeting.participants_count,
        })
    else:
        return JsonResponse({
            'id' : '',
            'room' : '',
            'start_date' : '',
            'start_time' : '',
            'duration': '',
            'participants_count': '',
        })


def get_room_schedule(request, id, *args, **kwargs):
    profile = Profile.objects.filter(pk=id).first()
 
    if profile is not None:
        meetings_list = get_room_schedule_meetings_list(profile.user)
        meetings_list_json = json.dumps(
            [{'creator': meeting.creator.public_name if meeting.creator else None,
             'name': meeting.name,
             'start_date': meeting.start_date_str(),
             'start_time': meeting.start_time_str(), 
             'end_time': meeting.end_time_str(),
             'background_colour': meeting.background_colour(),
             } for meeting in meetings_list])


        return HttpResponse(meetings_list_json, content_type="application/json")
    else:
        return HttpResponse("[]", content_type="application/json")

# --------------- Helper Functions ---------------
def get_room_schedule_meetings_list(user: User) -> list:
    meetings_list = RoomManager.get_room_meeting_list_today_after_hour(user, datetime.now().time().hour)
    padded_meetings_list = __pad_with_free_meetings(meetings_list)
    return padded_meetings_list

# If there is time between meetings, insert 'ghost' meetings saying that the room is free.
def __pad_with_free_meetings(meeting_list: list) -> list:
    today = datetime.now().date()

    # Start from 00th minute of the current hour
    current_time = datetime.now().time()
    current_time = current_time.replace(hour=current_time.hour, minute=0, second=0, microsecond=0)

    current_date_time = datetime.combine(today, current_time).astimezone()
    
    
    # If we have no meetings, return only one ghost meeting until midnight.
    if len(meeting_list) == 0:      
        return [__create_ghost_meeting(today, current_time, __time_until_midnight(current_time))]


    padded_meetings_list = []

    # If the first meeting is in the future, insert a Ghost meeting before it
    if not meeting_list[0].is_currently_ongoing():
        first_meeting = meeting_list[0]
        padded_meetings_list.append(__create_ghost_meeting(today, current_time, __time_until_meeting(first_meeting, current_date_time)))


    for i in range(0, len(meeting_list)-1):
        curr_meeting = meeting_list[i]
        next_meeting = meeting_list[i+1]

        # time_between_mins = (next_meeting.start_date_time() - curr_meeting.end_date_time()).total_seconds() // 60
        time_between_mins = __time_until_meeting(next_meeting, curr_meeting.end_date_time())

        padded_meetings_list.append(curr_meeting)

        if(time_between_mins >= 1):
            padded_meetings_list.append(__create_ghost_meeting(today, curr_meeting.end_time(), time_between_mins))


    last_meeting = meeting_list[-1]
    padded_meetings_list.append(last_meeting)
    
    #  if the last meeting does not go over 24:00, append one more padded meeting
    if last_meeting.start_date_time().day == last_meeting.end_date_time().day:      
        padded_meetings_list.append(__create_ghost_meeting(today, last_meeting.end_time(), __time_until_midnight(last_meeting.end_time())))

    return padded_meetings_list

def __create_ghost_meeting(start_date: datetime.date, start_time: datetime.time, duration: int):
    room_free_text = 'Room Is Free!'
    return Meeting(creator=None, room=None, name=room_free_text, 
        start_date=start_date, start_time=start_time,
        duration=duration, participants_count=0)

def __time_until_meeting(meeting: Meeting, current_date_time: datetime):
    return (meeting.start_date_time() - current_date_time).total_seconds() // 60

def __time_until_midnight(curr_time: datetime.time):
    return 1439 - (curr_time.hour * 60 + curr_time.minute)

