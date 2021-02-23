from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Meeting, SystemConstants
from .meeting_distance_types import MeetingDistanceTypes
from accounts.user_types import UserTypes
from .location_models import Building

class RoomManager:
    @staticmethod
    def schedule_meeting(meeting_name:str, number_attendees:int , start_date: datetime.date, start_time: datetime.time, duration: int, creator:User):
        # todo1: RoomManager.purge_old_meetings()

        if creator.profile.floor is None:
            return None, "Can't book a room as your location has not been set!"

        chosen_room = RoomManager.__choose_smallest_free_room(number_attendees, start_date, start_time, duration, creator.profile)

        if chosen_room is None:
            return None, 'There is no free room for the chosen time!'
        
        return Meeting.objects.create(name=meeting_name, creator=creator.profile, room=chosen_room, start_date=start_date, start_time=start_time, duration=duration, participants_count=number_attendees), None
        

    @staticmethod
    def __choose_smallest_free_room(number_attendees: int, start_date: datetime.date, start_time: datetime.time, duration: int, user_profile: Profile) -> Profile:
        rooms = RoomManager.get_free_rooms(number_attendees, user_profile)
        
        print("--- Free rooms after distance is set ---")
        RoomManager.__print_free_rooms(rooms, start_date, start_time, duration)

        # rooms are sorted by capacity, so the first free room will be the smallest one possible
        for room in rooms:
            if room.is_free(start_date, start_time, duration):
                return room
        return None


    @staticmethod
    def get_free_rooms(number_attendees: int, user_profile: Profile):
        rooms = Profile.objects.filter(type__exact=UserTypes.room).filter(capacity__gte=number_attendees).order_by('capacity')
        # todo1: synchronization? atomicity?

        rooms = RoomManager.__filter_rooms_by_distance(rooms, user_profile)

        return rooms


    @staticmethod
    def __filter_rooms_by_distance(rooms, creator_profile):
        # only check rooms that have location set
        location_rooms = [room for room in rooms if room.floor is not None]
        
        filter_rooms_lambda = lambda room: True
        constants = SystemConstants.get_constants()

        if constants.distance_type == MeetingDistanceTypes.same_floor:
            print("Distance type: same floor")
            filter_rooms_lambda = lambda room: bool(room.floor.id == creator_profile.floor.id)
        elif constants.distance_type == MeetingDistanceTypes.same_building:
            print("Distance type: same building")
            filter_rooms_lambda = lambda room: bool(room.floor.building.id == creator_profile.floor.building.id)
        elif constants.distance_type == MeetingDistanceTypes.number_floors:
            floors_distance = constants.distance_floors
            print(f"Distance type: number floors {floors_distance}")
            filter_rooms_lambda = lambda room: bool(room.floor.building.id == creator_profile.floor.building.id \
                and abs(room.floor.actual_floor - creator_profile.floor.actual_floor)<=floors_distance)
        elif constants.distance_type == MeetingDistanceTypes.near_buildings:
            print("Distance type: near buildings")
            
            inb = SystemConstants.get_constants().infer_nearby_buildings
            print(f"Infer nearby buildings : {inb}")

            building_ids = RoomManager.__get_near_building_ids_infer(creator_profile) if inb \
                else RoomManager.__get_near_building_ids(creator_profile)
            print(f"Near building ids: {building_ids}")

            # logging purposes 
            for bid in building_ids:
                print(f"ID {bid} = {Building.objects.get(pk=bid).name}")

            filter_rooms_lambda = lambda room: bool(room.floor.building.id in building_ids)

        return [r for r in location_rooms if filter_rooms_lambda(r)]

    @staticmethod
    def __get_near_building_ids(creator_profile):
        near_buildings = creator_profile.floor.building.get_near_buildings()
        return  set([building.id for building in near_buildings])

    @staticmethod
    def __get_near_building_ids_infer(creator_profile):
        near_buildings = creator_profile.floor.building.get_near_buildings_infer()
        return set([nb.id for nb in near_buildings])
    

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