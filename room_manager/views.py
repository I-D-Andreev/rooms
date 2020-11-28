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

    return render(request, f'room_manager/{dashboard}_dashboard.html')


@login_required(login_url='login')
@user_only
def statistics_view(request, *args, **kwargs):
    return render(request, f'room_manager/user/statistics.html')
