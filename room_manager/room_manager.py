from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Meeting
from accounts.user_types import UserTypes

class RoomManager:
    @staticmethod
    def schedule_meeting(meeting_name:str, number_attendees:int , start_date: datetime.date, start_time: datetime.time, duration: int, creator:User):
        rooms = Profile.objects.filter(type__exact=UserTypes.room).filter(capacity__gte=number_attendees).order_by('capacity')

        # todo1: RoomManager.purge_old_meetings()

        # rooms are sorted by capacity, so the first free room will be the smallest one possible
        chosen_room = RoomManager.__choose_first_free_room(rooms, start_date, start_time, duration)

        if chosen_room is None:
            return None
        
        return Meeting.objects.create(name=meeting_name, creator=creator.profile, room=chosen_room, start_date=start_date, start_time=start_time, duration=duration, participants_count=number_attendees)
        


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
    def get_user_meetings_list_from_now(user: User) -> list:
        # todo1: Group meetings by start_date and display the schedule in a better way
        now = datetime.now().astimezone()

        all_meetings = user.profile.user_meetings.all().order_by('start_date', 'start_time')

        filtered_meetings = []
        for meeting in all_meetings:
            if meeting.start_date_time() >= now:
                filtered_meetings.append(meeting)
        
        return filtered_meetings

    
    @staticmethod
    def get_user_meetings_list_today(user: User) -> list:
        today = date.today()
        return user.profile.user_meetings.filter(start_date__exact=str(today)).order_by('start_time')


    @staticmethod
    def get_room_meeting_list_today(room: User) -> list:
        if room.profile.type != UserTypes.room:
            return []
        
        today = date.today()
        return room.profile.meetings.filter(start_date__exact=str(today)).order_by('start_time')

    
    
    # Get the meetings today starting from the 00th minute of the current hour.
    @staticmethod
    def get_room_meeting_list_today_after_hour(room: User, current_hour: int) -> list:
        if room.profile.type != UserTypes.room:
            return []
        
        meetings_today = RoomManager.get_room_meeting_list_today(room)

        meetings_from_current_hour = []

        for meeting in meetings_today:
            if meeting.start_time.hour >= current_hour:
                meetings_from_current_hour.append(meeting)
        
        return meetings_from_current_hour