from accounts.decorators import room_only
from django.contrib.auth.decorators import login_required
from .room_manager import RoomManager
from django.shortcuts import render
from .room_forms import CancelMeetingForm
from django.contrib import messages
from accounts.models import Profile
from .room_forms import BookNowForm


@login_required(login_url='login')
@room_only
def book_now_view(request, *args, **kwargs):
    profile_id = request.POST.get('id', None) if request.method == "POST" else request.GET.get('id', None)
    profile = None if not profile_id else Profile.objects.filter(pk=profile_id).first()

    form = BookNowForm()

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
                form = BookNowForm()
            else:
                messages.error(request, "Booking failed!")

         
    context = {'form': form, 'profile': profile}
    return render(request, 'room_manager/room/book_now.html', context)


@login_required(login_url='login')
@room_only
def nearest_room_view(request, *args, **kwargs): # Similar Rooms
    room_profile = request.user.profile
    rooms = RoomManager.get_rooms_free_now(room_profile.capacity, room_profile)

    context = {'rooms': rooms}
    return render(request, 'room_manager/room/nearest_room.html', context)


@login_required(login_url='login')
@room_only
def cancel_meeting_view(request, *args, **kwargs):
    form = CancelMeetingForm(user=request.user)

    if request.method == "POST":
        form = CancelMeetingForm(request.POST, user=request.user)

        if form.is_valid():
            resp = form.try_cancel_meeting()

        
        if resp:
            messages.success(request, "Successfully cancelled the meeting!")
            form = CancelMeetingForm(user=request.user)
        else:
            messages.error(request, "Failed to cancel the meeting!")

    context = {'form': form}
    return render(request, 'room_manager/room/cancel_meeting.html', context)

