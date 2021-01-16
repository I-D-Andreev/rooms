from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from room_manager.decorators import user_only
from accounts.forms import UserRegistrationForm
from accounts.user_types import UserTypes


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


# login + admin only
def create_room_view(request, *args, **kwargs):
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        edited_request = request.POST.copy()
        edited_request.update({'type': UserTypes.room})

        form = UserRegistrationForm(edited_request)

        if form.is_valid():
            print("form is valid")
            form.save()
        else:
            print('form is not valid')
            print(form.errors)
            # user = form.save()
            # login(request, user)
            # return redirect(dashboard_view)

    args = {'form': form}
    return render(request, 'room_manager/admin/create_room.html', args)
    