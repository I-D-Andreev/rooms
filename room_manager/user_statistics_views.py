from django.shortcuts import render
from .user_forms import ChooseRoomForm
from .room_manager import RoomManager
from .models import SystemConstants
from datetime import datetime, timedelta

# @login_required(login_url='login')
# @user_only
def statistics_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/statistics/statistics.html')

# login + user only
def room_utilization_statistics_view(request, *args, **kwargs):
    form = ChooseRoomForm()

    daily_percentage_utilization = __calculate_rooms_utilization_data_weekly()
    
    context = {'form': form, 'daily_utilization': daily_percentage_utilization}
    return render(request, 'room_manager/user/statistics/room_utilization.html', context)


def __calculate_rooms_utilization_data_weekly():
    data = {}
    minutes_in_working_day = SystemConstants.get_num_working_minutes()
    last_seven_days = __last_seven_days_array()

    rooms = RoomManager.get_all_rooms()
    
    for room in rooms:
        utilization_percentages = []

        for day in last_seven_days:
            minutes_booked = room.minutes_booked_at(day)
            utilization_percentages.append((minutes_booked/minutes_in_working_day) * 100)

        data.update({room.id: utilization_percentages})
    
    data["days"] = [__format_day(d) for d in last_seven_days]

    return data


def __last_seven_days_array():
    start_date = datetime.now() - timedelta(days=6)
    last_seven_days = []

    for _ in range(7):
        last_seven_days.append(start_date.date())
        start_date += timedelta(days=1)

    return last_seven_days


def __format_day(day: datetime.day):
    d = f"{day.day}" if day.day > 9 else f"0{day.day}"
    m = f"{day.month}" if day.month > 9 else f"0{day.month}"
    return f"{d}.{m}"
    