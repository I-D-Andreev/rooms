from django.db import models 
from django.contrib.auth.models import User
from django.db.models.fields import related
from accounts.user_types import UserTypes
from datetime import datetime, time, timedelta, timezone

from room_manager.location_models import Floor

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=UserTypes.as_choice_list())
    capacity = models.IntegerField(default=0)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, related_name="profiles")


# to add location and room-type
    def __str__(self):
        return self.public_name


    def is_free(self, start_date: datetime.date, start_time: datetime.time, duration:int) -> bool:
        if self.type != UserTypes.room:
            return False
  
        start_date_time = datetime.combine(start_date, start_time).astimezone()
        end_date_time = start_date_time + timedelta(minutes=duration)

        # remove one minute because of overlapping meetings that start on the exact hour
        start_date_time = start_date_time + timedelta(minutes=1)
        end_date_time = end_date_time + timedelta(minutes=-1)

        booked_meetings = self.meetings.all()

        for meeting in booked_meetings:
            if start_date_time < meeting.end_date_time() and \
                end_date_time > meeting.start_date_time():
                return False

        return True
    

    def is_free_now(self):
        if self.type != UserTypes.room:
            return False
        
        current_date_time = datetime.now().astimezone()
        booked_meetings = self.meetings.all()
        
        for meeting in booked_meetings:
            if current_date_time >= meeting.start_date_time() and \
                current_date_time <= meeting.end_date_time():
                return False
        
        return True

    def meeting_now(self):
        if self.type != UserTypes.room:
            return None
        
        current_date_time = datetime.now().astimezone()
        booked_meetings = self.meetings.all()

        for meeting in booked_meetings:
            if current_date_time >= meeting.start_date_time() and \
                current_date_time <= meeting.end_date_time():
                return meeting
        
        return None


    def free_up_to(self) -> time:
        if self.type != UserTypes.room:
            return None
        
        
        current_date_time = datetime.now().astimezone()
        future_meetings_today = [meeting for meeting in self.meetings.all()
             if meeting.in_future() and meeting.start_date == current_date_time.date()]
        
        up_to = time(hour=23, minute=59)
        for fm in future_meetings_today:
            up_to = min(up_to, fm.start_date_time().time())

        return up_to

    def free_up_to_formatted(self) -> str:
        return self.__format_time(self.free_up_to())


    def __format_time(self, time: datetime.time):
        hours = f"0{time.hour}" if time.hour < 10 else f"{time.hour}"
        minutes = f"0{time.minute}" if time.minute < 10 else f"{time.minute}"
        return f"{hours}:{minutes}"

    
    def minutes_booked_at(self, day: datetime.day):
        if self.type != UserTypes.room:
            return 0
        
        minutes_booked = 0

        meetings = self.meetings.all()
        for meeting in meetings:
            if meeting.happens_at_day(day):
                minutes_booked += meeting.duration
        
        return minutes_booked