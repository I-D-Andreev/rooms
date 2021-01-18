from datetime import datetime, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Meeting
from accounts.user_types import UserTypes

class RoomManager:
    @staticmethod
    def schedule_meeting(number_attendees:int , date: datetime.date, time: datetime.time, duration: int, creator:User):
        rooms = Profile.objects.filter(type__exact=UserTypes.room).filter(capacity__gte=number_attendees).order_by('capacity')
        start_time = datetime.combine(date, time).astimezone()

        # remove a minute from the duration so that a meeting finishing at 
        # (e.g.) 14:00 will not stop another meeting booked to start at 14:00
        end_time = (start_time + timedelta(minutes=(duration-1))).astimezone()

        # todo1: RoomManager.purge_old_meetings()

        # rooms are sorted by capacity, so the first free room will be the smallest one possible
        chosen_room = RoomManager.__choose_first_free_room(rooms, start_time, end_time)

        if chosen_room is None:
            return None
        
        return Meeting.objects.create(creator=creator.profile, room=chosen_room, start_time=start_time, end_time=end_time, participants_count=number_attendees)
        


    def __choose_first_free_room(rooms, start_time: datetime.time, end_time: datetime.time) -> Profile:
        # todo1: synchronization?
        RoomManager.__print_free_rooms(rooms, start_time, end_time)

        for room in rooms:
            if room.is_free(start_time, end_time):
                return room
        return None


    # for testing purposes
    @staticmethod
    def __print_free_rooms(rooms, start_time: datetime.time, end_time: datetime.time):
        for room in rooms:
            is_free = 'free' if room.is_free(start_time, end_time) else 'not free'
            print(f"Room {room.public_name} (capacity {room.capacity}) is {is_free}")


    @staticmethod
    def purge_old_meetings():
        # todo1: purge meetings older than 3? months
        pass