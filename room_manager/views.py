from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    dashboard = 'no_access'
    try:
        dashboard = request.user.profile.type
    except ObjectDoesNotExist:
        pass

    return render(request, f'room_manager/{dashboard}_dashboard.html')
