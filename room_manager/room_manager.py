from accounts.models import Profile
from accounts.user_types import UserTypes
from datetime import datetime, timedelta

class RoomManager:
    def __init__(self, number_attendees:int , date: datetime.date, time: datetime.time, duration: int):
        self.rooms = Profile.objects.filter(type__exact=UserTypes.room).filter(capacity__gte=number_attendees).order_by('capacity')
        self.start_time = datetime.combine(date, time)

        # remove a minute from the duration so that a meeting finishing at 
        # (e.g.) 14:00 will not stop another meeting booked to start at 14:00
        self.end_time = self.start_time + timedelta(minutes=(duration-1))

        self.purge_old_meetings()


    def purge_old_meetings(self):
        # todo1: meetings older than 3 months? to be removed
        pass


    def __choose_room(self):
        # todo1: synchronization?
        for room in self.rooms:
            if room.is_free(self.start_time, self.end_time):
                return room        
        return None
    
    # def schedule_meeting(self):
    #     room = self.__choose_room()



    def print(self):
        for x in self.rooms:
            print(f"Room {x.public_name} (type {x.type}) has a capacity of {x.capacity}")


    def print_range(self):
        print(f"Start time: {self.start_time}")
        print(f"End time: {self.end_time}")


    def free_rooms(self):
        for room in self.rooms:
            is_free = 'free' if room.is_free(self.start_time, self.end_time) else 'not free'
            print(f"Room {room.public_name} is {is_free}")
