from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.user_groups import UserGroups


@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    dashboard = 'no_access'
    if request.user.groups.exists():
        group_name = None
        for group in request.user.groups.all():
            if group.name in UserGroups.as_list():
                group_name = group.name
                break

        if group_name == UserGroups.admins:
            dashboard = 'admin'
        elif group_name == UserGroups.users:
            dashboard = 'user'
        elif group_name == UserGroups.rooms:
            dashboard = 'room'

    return render(request, f'room_manager/{dashboard}_dashboard.html')
