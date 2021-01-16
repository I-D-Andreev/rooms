from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from room_manager.decorators import user_only


@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    try:
        dashboard = request.user.profile.type
    except ObjectDoesNotExist:
        raise PermissionDenied()

    args = {'username': request.user.username}
    return render(request, f'room_manager/{dashboard}_dashboard.html', args)


@login_required(login_url='login')
@user_only
def statistics_view(request, *args, **kwargs):
    return render(request, 'room_manager/user/statistics.html')


def create_room_view(request, *args, **kwargs):
    return render(request, 'room_manager/admin/create_room.html')