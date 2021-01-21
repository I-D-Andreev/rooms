from django.db import models
from django.contrib.auth.models import User
from accounts.user_types import UserTypes
from datetime import datetime, time, timedelta, timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=UserTypes.as_choice_list())
    capacity = models.IntegerField(default=0)

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
