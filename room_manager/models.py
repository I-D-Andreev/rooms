from datetime import datetime, timedelta
from django.db import models
from accounts.models import Profile


class Meeting(models.Model):
    creator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='user_meetings')
    room = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='meetings')
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField()
    participants_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.room.public_name} | {self.start_time_str()}"

    def long_name(self):
        return f"{self.creator.public_name}-{self.room.public_name}| {self.start_time_str()} | {self.end_time_str()}"    

    def start_date_time(self):
        return datetime.combine(self.start_date, self.start_time).astimezone()

    def end_date_time(self):
        return (self.start_date_time() + timedelta(minutes=self.duration))

    def start_time_str(self):
        return self.__format_time(self.start_date_time())

    def end_time_str(self):
        return self.__format_time(self.end_date_time())


    def __format_time(self, time: datetime):
        return time.strftime('%Y-%m-%d %H:%M')