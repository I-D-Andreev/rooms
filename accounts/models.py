from django.db import models
from django.contrib.auth.models import User
from accounts.user_types import UserTypes
from datetime import datetime, tzinfo

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=UserTypes.as_choice_list())
    capacity = models.IntegerField(default=0)

# to add location and room-type
    def __str__(self):
        return self.public_name


    def is_free(self, start_time: datetime, end_time: datetime) -> bool:
        if self.type != UserTypes.room:
            return False
        
        booked_meetings = self.meetings.all()

        for meeting in booked_meetings:
            if start_time < meeting.end_time and \
                end_time > meeting.start_time:
                return False

        return True
        