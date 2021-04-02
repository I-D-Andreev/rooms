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

    daily_percentage_utilization = __calculate_rooms_utilization_data_daily()
    weekly_percentage_utilization = __calculate_rooms_utilization_data_weekly()
    
    context = {'form': form, 'daily_utilization': daily_percentage_utilization, 'weekly_utilization': weekly_percentage_utilization}
    return render(request, 'room_manager/user/statistics/room_utilization.html', context)

def __calculate_rooms_utilization_data_weekly():
    data = {}
    minutes_in_working_week = SystemConstants.get_num_working_minutes() * 5
    last_seven_weeks = __last_seven_weeks_array()

    rooms = RoomManager.get_all_rooms()

    for room in rooms:
        utilization_percentages = []

        for week in last_seven_weeks:
            minutes_booked = room.minutes_booked_between(week[0], week[1])
            utilization_percentages.append((minutes_booked/minutes_in_working_week) * 100)

        data.update({room.id: utilization_percentages})
    
    data["weeks"] = [f"Week {w[2]}" for w in last_seven_weeks]

    return data



def __calculate_rooms_utilization_data_daily():
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
    print("Called")
    print(f"Date: {datetime.now()}")
    start_date = datetime.now() - timedelta(days=6)
    last_seven_days = []

    for _ in range(7):
        last_seven_days.append(start_date.date())
        start_date += timedelta(days=1)

    return last_seven_days


def __last_seven_weeks_array():
    start_date = datetime.now() - timedelta(weeks=6)
    last_seven_weeks = []

    for _ in range(7):
        st, en = __start_end_of_week(start_date)
        last_seven_weeks.append((st,en, __get_week_number(start_date)))
        start_date += timedelta(weeks=1)
    
    return last_seven_weeks



def __start_end_of_week(day: datetime):
    week_start = (day - timedelta(days=day.weekday())).date()
    week_end = week_start + timedelta(days=6)

    return week_start, week_end

def __get_week_number(day: datetime):
    return day.isocalendar()[1]


def __format_day(day: datetime.day):
    d = f"{day.day}" if day.day > 9 else f"0{day.day}"
    m = f"{day.month}" if day.month > 9 else f"0{day.month}"
    return f"{d}.{m}"
    