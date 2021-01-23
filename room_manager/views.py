from django.contrib.messages.api import success
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from room_manager.decorators import user_only
from accounts.forms import UserRegistrationForm
from accounts.user_types import UserTypes
from django.contrib import messages
from .user_forms import BookRoomForm, DeleteMeetingForm
from .room_manager import RoomManager
from django.http import JsonResponse
from .models import Meeting
from datetime import datetime
from django.contrib.auth.models import User


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

    context = {'form': form}
    return render(request, 'room_manager/admin/create_room.html', context)


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
                messages.info(request, 'There is no free room for the chosen time!')
            else:
                messages.info(request, f"Successfully booked room {meeting.room.public_name} from {meeting.start_time_str()} to {meeting.end_time_str()}.")
                form = BookRoomForm()


    context = {'form': form}
    return render(request, 'room_manager/user/book_room.html', context)

# login + user only
def cancel_booking_view(request, *args, **kwargs):

    if request.method == 'POST':
        meeting_id = request.POST['meeting']
        meeting = Meeting.objects.filter(pk=meeting_id).first()
        
        message = 'Failed to cancel the booking!'
        if meeting is not None:
            resp = meeting.delete()
            if resp[0] >= 1:
                message = f'The booking has been successfully cancelled!\n {meeting.long_name()}'

        messages.info(request, message)

    form = DeleteMeetingForm(user=request.user)
    context  = {'form': form}
    return render(request, 'room_manager/user/cancel_booking.html', context)

# login + user only
def my_schedule_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/my_schedule.html')
    



def get_meeting(request, id, *args, **kwargs):
    meeting = Meeting.objects.filter(pk=id).first()

    print(request.headers)
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

def get_room_schedule_meetings_list(user: User) -> list:
    current_hour = datetime.now().time().hour if user.profile.is_free_now() else user.profile.meeting_now().start_time.hour
    meetings_list = RoomManager.get_room_meeting_list_today_after_hour(user, current_hour)
    padded_meetings_list = __pad_with_free_meetings(meetings_list)

    return padded_meetings_list

# If there is time between meetings, insert 'ghost' meetings saying that the room is free.
def __pad_with_free_meetings(meeting_list: list) -> list:
    room_free_text = 'Room Is Free!'

    # If we have no meetings, return only one ghost meeting until midnight.
    if len(meeting_list) == 0:
        current_time = datetime.now().time()
        # Start from 00th minute of the current hour
        current_time = current_time.replace(hour=current_time.hour, minute=0, second=0, microsecond=0)

        return [Meeting(creator=None, room=None, name=room_free_text,
            start_date=None, start_time=current_time,
            duration=__time_until_midnight(current_time),
            participants_count=0)]


    padded_meetings_list = []
    for i in range(0, len(meeting_list)-1):
        curr_meeting = meeting_list[i]
        next_meeting = meeting_list[i+1]

        time_between_mins = (next_meeting.start_date_time() - curr_meeting.end_date_time()).total_seconds() // 60

        padded_meetings_list.append(curr_meeting)

        if(time_between_mins >= 1):
            padded_meetings_list.append(Meeting(creator=None, room=None, 
            name=room_free_text, start_date=None,
            start_time = curr_meeting.end_time(),
            duration=time_between_mins, participants_count=0))


    last_meeting = meeting_list[-1]
    padded_meetings_list.append(last_meeting)
    
    #  if the last meeting does not go over 24:00, append one more padded meeting
    if last_meeting.start_date_time().day == last_meeting.end_date_time().day:
        padded_meetings_list.append(Meeting(creator=None, room=None, 
            name=room_free_text, start_date=None,
            start_time = last_meeting.end_time(), 
            duration=__time_until_midnight(last_meeting.end_time()),
             participants_count=0))

    return padded_meetings_list

def __time_until_midnight(curr_time: datetime.time):
    return 1439 - (curr_time.hour * 60 + curr_time.minute)

