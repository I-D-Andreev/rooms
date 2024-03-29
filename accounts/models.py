from django.db import models 
from django.contrib.auth.models import User
from datetime import datetime, time, timedelta, timezone
from django.urls import reverse
from accounts.user_types import UserTypes

from room_manager.location_models import Floor
from .unique_code import UniqueCode

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
        return self.minutes_booked_between(day, day)


    def minutes_booked_between(self, start: datetime.date, end: datetime.date):
        if self.type != UserTypes.room:
            return 0

        minutes_booked = 0

        meetings = self.meetings.all()
        for meeting in meetings:
            if meeting.happens_between(start,end):
                minutes_booked += meeting.duration
        
        return minutes_booked

    def meetings_ongoing_or_in_future(self):
        if self.type != UserTypes.room:
            return []
        
        all_meetings = self.meetings.all()
        return [meeting for meeting in all_meetings if not meeting.has_passed()]


class RegistrationLink(models.Model):
    type = models.CharField(max_length=255, choices=UserTypes.user_admin_choice_list())
    unique_code = models.CharField(max_length=100)
    valid_until = models.DateTimeField()

    @staticmethod
    def create_registration_link(account_type, time_to_live):
        try:
            RegistrationLink.purge_old_links()

            if (account_type not in [UserTypes.user, UserTypes.admin]) or time_to_live <= 0:
                return None
            
            ttl_date = datetime.now().astimezone() + timedelta(minutes=time_to_live)
            code = UniqueCode.generate_unique_code()
            return RegistrationLink.objects.create(type=account_type, unique_code = code, valid_until = ttl_date)
        except Exception as e:
            print(f"Exception: {e}")
            return None


  
    def get_full_url(self, request):
        return request.build_absolute_uri(reverse("register", kwargs={'code': self.unique_code}))

    def valid_until_formatted(self):
        return self.valid_until.strftime("%d.%m.%Y, %H:%M")


    @staticmethod
    def get_all_valid_links():
        now = datetime.now().astimezone()
        return RegistrationLink.objects.filter(valid_until__gte=now)

    @staticmethod
    def purge_old_links():
        if RegistrationLink.objects.count() >= 100:
            now = datetime.now().astimezone()
            RegistrationLink.objects.filter(valid_until__lte=now).delete()
            print("Registration Links Purged")



class ForgottenPasswordLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="forgotten_password_links")
    unique_code = models.CharField(max_length=100)
    valid_until = models.DateTimeField()

    @staticmethod
    def create_forgotten_password_link(profile, time_to_live):
        try:
            ForgottenPasswordLink.purge_old_links()

            ttl_date = datetime.now().astimezone() + timedelta(minutes=time_to_live)
            code = UniqueCode.generate_unique_code()
            return ForgottenPasswordLink.objects.create(profile=profile, unique_code=code, valid_until=ttl_date)
        except Exception as e:
            print(f"Exception: {e}")
            return None


    def get_full_url(self, request):
        return request.build_absolute_uri(reverse("reset_password", kwargs={'code': self.unique_code}))

    def valid_until_formatted(self):
        return self.valid_until.strftime("%d.%m.%Y, %H:%M")

    
    @staticmethod
    def get_all_valid_links():
        now = datetime.now().astimezone()
        return ForgottenPasswordLink.objects.filter(valid_until__gte=now)


    @staticmethod
    def purge_old_links():
        if ForgottenPasswordLink.objects.count() >= 100:
            now = datetime.now().astimezone()
            ForgottenPasswordLink.objects.filter(valid_until__lte=now).delete()
            print("Forgotten Password Links Purged")