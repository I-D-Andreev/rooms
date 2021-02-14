from datetime import datetime, date, timedelta
from django.db import models
from accounts.models import Profile
from .meeting_distance_types import MeetingDistanceTypes

class Meeting(models.Model):
    creator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='user_meetings')
    room = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='meetings')
    name = models.CharField(max_length=150)
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField()
    participants_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} | {self.start_date_time_str()}"

    def long_name(self):
        return f"User: {self.creator.public_name} | Name: {self.name} | Room: {self.room.public_name} | From: {self.start_date_time_str()} | To: {self.end_date_time_str()}"    

    def end_date(self):
        return self.end_date_time().date()

    def start_date_time(self):
        return datetime.combine(self.start_date, self.start_time).astimezone()

    def end_date_time(self):
        return (self.start_date_time() + timedelta(minutes=self.duration))

    def end_time(self):
        # workaround as timedelta does not work for datetime.time objects
        dt = datetime.combine(date.today(), self.start_time)
        dt = dt + timedelta(minutes=self.duration)
        return dt.time()

    def start_date_time_str(self):
        return self.__format_date_time(self.start_date_time())

    def end_date_time_str(self):
        return self.__format_date_time(self.end_date_time())

    def start_time_str(self):
        return self.__format_time(self.start_time)
    
    def end_time_str(self):
     return self.__format_time(self.end_time())

    def start_date_str(self):
        return self.__format_date(self.start_date)

    def __format_date(self, dd: datetime.date):
        return f"{dd.year}-{dd.month}-{dd.day}"

    def __format_time(self, time: datetime.time):
        hours = f"0{time.hour}" if time.hour < 10 else f"{time.hour}"
        minutes = f"0{time.minute}" if time.minute < 10 else f"{time.minute}"
        return f"{hours}:{minutes}"

    def __format_date_time(self, dtime: datetime):
        return dtime.strftime('%Y-%m-%d %H:%M')
    
    def has_passed(self):
        now = datetime.now().astimezone() + timedelta(minutes=1)
        return (now > self.end_date_time())

    def is_currently_ongoing(self):
        now = datetime.now().astimezone()
        return (now >= self.start_date_time() and now <= self.end_date_time())

    def background_colour(self):
        if self.is_currently_ongoing():
            if self.creator is None:
                return 'bg-green'
            else:
                return 'bg-light-red'
        else:
            return 'bg-white'


# Only one instance will be stored. Will keep track of system constants.
class SystemConstants(models.Model):
    distance_type = models.CharField(choices=MeetingDistanceTypes.as_choice_list(), max_length=255)
    distance_floors = models.PositiveIntegerField()


    @staticmethod
    def get_constants():
        constants = SystemConstants.objects.first()

        if constants is None:
            constants = SystemConstants.__create_default_constants()
        
        return constants


    @staticmethod
    def __create_default_constants():
        return SystemConstants.objects.create(distance_type=MeetingDistanceTypes.same_building, distance_floors=0)


    @staticmethod
    def update_meeting_room_distance_constants(distance_type: str, distance_floors:int = 0):
        if distance_type != MeetingDistanceTypes.number_floors:
            distance_floors = 0
        
        print(distance_type)
        print(distance_floors)

        constants = SystemConstants.get_constants()
        constants.distance_type = distance_type
        constants.distance_floors = distance_floors
        constants.save()
