from .room_manager import RoomManager
from django.shortcuts import render
from .room_forms import CancelMeetingForm
from django.contrib import messages


# login + room only
def nearest_room_view(request, *args, **kwargs): # Similar Rooms
    room_profile = request.user.profile
    rooms = RoomManager.get_rooms_free_now(room_profile.capacity, room_profile)

    context = {'rooms': rooms}
    return render(request, 'room_manager/room/nearest_room.html', context)


# login + room only
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

