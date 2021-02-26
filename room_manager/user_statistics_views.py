from django.shortcuts import render

# @login_required(login_url='login')
# @user_only
def statistics_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/statistics/statistics.html')