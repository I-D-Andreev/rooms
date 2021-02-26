from django.shortcuts import render

# @login_required(login_url='login')
# @user_only
def statistics_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/statistics/statistics.html')

# login + user only
def room_utilization_statistics_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/statistics/room_utilization.html')
