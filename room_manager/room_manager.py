from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Meeting
from accounts.user_types import UserTypes

class RoomManager:
    @staticmethod
    def schedule_meeting(meeting_name:str, number_attendees:int , start_date: datetime.date, start_time: datetime.time, duration: int, creator:User):
        # todo1: RoomManager.purge_old_meetings()

        chosen_room = RoomManager.__choose_smallest_free_room(number_attendees, start_date, start_time, duration)

        if chosen_room is None:
            return None
        
        return Meeting.objects.create(name=meeting_name, creator=creator.profile, room=chosen_room, start_date=start_date, start_time=start_time, duration=duration, participants_count=number_attendees)
        


    def __choose_smallest_free_room(number_attendees: int, start_date: datetime.date, start_time: datetime.time, duration: int) -> Profile:
        rooms = Profile.objects.filter(type__exact=UserTypes.room).filter(capacity__gte=number_attendees).order_by('capacity')

        # todo1: synchronization?
        RoomManager.__print_free_rooms(rooms, start_date, start_time, duration)
        
        # rooms are sorted by capacity, so the first free room will be the smallest one possible
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
    def try_book_room_now(room: User, name:str, duration:int) -> bool:
        curr_date = datetime.now().date()
        curr_time = datetime.now().time()

        if RoomManager.can_book_room_now(room, curr_date, curr_time, duration):
            return Meeting.objects.create(name=name, creator=room.profile, room=room.profile, start_date=curr_date, start_time=curr_time, duration=duration, participants_count=0)
            
        return None


    @staticmethod
    def can_book_room_now(room: User, curr_date: datetime.date, curr_time: datetime.time, duration: int) -> bool: 
        return room.profile.is_free(curr_date, curr_time, duration)


    
    @staticmethod
    def get_user_meetings_list_from_now(user: User) -> list:
        now = datetime.now().astimezone()

        all_meetings = user.profile.user_meetings.all().order_by('start_date', 'start_time')

        filtered_meetings = []
        for meeting in all_meetings:
            if meeting.start_date_time() >= now or meeting.is_currently_ongoing():
                filtered_meetings.append(meeting)
        
        return filtered_meetings

    
    @staticmethod
    def get_user_meetings_list_today(user: User) -> list:
        # todo1: shall we do the same as get_room_meeting_list_today
        #  and get all meetings either ending today or starting today?
        today = date.today()
        return user.profile.user_meetings.filter(start_date__exact=str(today)).order_by('start_time')


    @staticmethod
    def get_room_meeting_list_today(room:User) -> list:
        if room.profile.type != UserTypes.room:
            return []
        
        today = date.today()
        all_meetings = room.profile.meetings.all().order_by('start_date', 'start_time')

        meetings_list = []
        for meeting in all_meetings:
            if meeting.start_date == today or meeting.end_date() == today:
                meetings_list.append(meeting)
        
        return meetings_list
    
    # Get the meetings that will happen today or are happening now (past meetings today are not displayed).
    @staticmethod
    def get_room_meeting_list_today_after_hour(room: User, current_hour: int) -> list:
        if room.profile.type != UserTypes.room:
            return []
        
        meetings_today = RoomManager.get_room_meeting_list_today(room)
        
        meetings_from_now = []

        for meeting in meetings_today:
            if meeting.start_time.hour >= current_hour or meeting.end_time().hour >= current_hour:
                meetings_from_now.append(meeting)
        
        return meetings_from_now