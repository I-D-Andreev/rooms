from django.db import models
from django.contrib.auth.models import User


from accounts.user_types import UserTypes


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=UserTypes.as_choice_list())
    capacity = models.IntegerField(default=0)

# to add location and room-type
    def __str__(self):
        return self.public_name
