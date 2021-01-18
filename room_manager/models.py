from datetime import datetime
from django.db import models
from accounts.models import Profile


class Meeting(models.Model):
    creator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='user_meetings')
    room = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='meetings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.creator.public_name}-{self.room.public_name}| {self.start_time_str()} | {self.end_time_str()}"

    def start_time_str(self):
        return self.__format_time(self.start_time)

    def end_time_str(self):
        return self.__format_time(self.end_time)

    def duration_minutes(self):
        diff = (self.end_time - self.start_time)
        return (diff.days * 1440) + (diff.seconds//60)

    def __format_time(self, time: datetime):
        return time.strftime('%Y-%m-%d %H:%M')