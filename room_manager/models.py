from django.db import models
from accounts.models import Profile


class Meeting(models.Model):
    creator = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='user_meetings')
    room = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='meetings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.creator.public_name}-{self.room.public_name}| {self.start_time} | {self.end_time}"
