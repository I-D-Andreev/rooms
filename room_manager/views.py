from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.user_groups import UserGroups


@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    dashboard = 'no_access'
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        if group == UserGroups.admins:
            dashboard = 'admin'
        elif group == UserGroups.users:
            dashboard = 'user'
        elif group == UserGroups.rooms:
            dashboard = 'room'

    return render(request, f'room_manager/{dashboard}_dashboard.html')
