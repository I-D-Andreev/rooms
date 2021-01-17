from django.db import models
from accounts.models import Profile


class Meeting(models.Model):
    creator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='meetingsc')
    room = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='meetingsr')
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField()  # in minutes
    participants_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.creator.public_name}-{self.room.public_name}| {self.date} | {self.time}"
