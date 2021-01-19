from datetime import datetime, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Meeting
from accounts.user_types import UserTypes

class RoomManager:
    @staticmethod
    def schedule_meeting(number_attendees:int , start_date: datetime.date, start_time: datetime.time, duration: int, creator:User):
        rooms = Profile.objects.filter(type__exact=UserTypes.room).filter(capacity__gte=number_attendees).order_by('capacity')

        # todo1: RoomManager.purge_old_meetings()

        # rooms are sorted by capacity, so the first free room will be the smallest one possible
        chosen_room = RoomManager.__choose_first_free_room(rooms, start_date, start_time, duration)

        if chosen_room is None:
            return None
        
        return Meeting.objects.create(creator=creator.profile, room=chosen_room, start_date=start_date, start_time=start_time, duration=duration, participants_count=number_attendees)
        


    def __choose_first_free_room(rooms, start_date: datetime.date, start_time: datetime.time, duration: int) -> Profile:
        # todo1: synchronization?
        RoomManager.__print_free_rooms(rooms, start_date, start_time, duration)

        for room in rooms:
            if room.is_free(start_date, start_time, duration):
                return room
        return None


    # for testing purposes
    @staticmethod
    def __print_free_rooms(rooms, start_date: datetime.date, start_time: datetime.time, duration: int):
        for room in rooms:
            is_free = 'free' if room.is_free(start_date, start_time, duration) else 'not free'
            print(f"Room {room.public_name} (capacity {room.capacity}) is {is_free}")


    @staticmethod
    def purge_old_meetings():
        # todo1: purge meetings older than 3? months
        pass

    
    @staticmethod
    def get_user_meetings_list(user: User) -> list:
        # todo1: Group meetings by start_date and display the schedule in a better way
        now = datetime.now().astimezone()

        all_meetings = user.profile.user_meetings.all().order_by('start_date', 'start_time')

        filtered_meetings = []
        for meeting in all_meetings:
            if meeting.start_date_time() >= now:
                filtered_meetings.append(meeting)
        
        return filtered_meetings

    