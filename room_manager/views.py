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
        meetings_list = None


    args = {'username': request.user.username, 'meetings_list': meetings_list}

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


    args = {'form': form}
    return render(request, 'room_manager/user/book_room.html', args)

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
    args  = {'form': form}
    return render(request, 'room_manager/user/cancel_booking.html', args)



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