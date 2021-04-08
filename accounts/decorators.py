from django.shortcuts import redirect
from accounts.user_types import UserTypes

def unauthenticated_user_only(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper


def admin_only(view_function):
    return certain_account_type_only(view_function, UserTypes.admin)


def room_only(view_function):
    return certain_account_type_only(view_function, UserTypes.room)


def user_only(view_function):
    return certain_account_type_only(view_function, UserTypes.user)


def certain_account_type_only(view_function, acc_type):
    def wrapper(request, *args, **kwargs):
        if (not hasattr(request.user, 'profile')) or (request.user.profile.type != acc_type):
            return redirect('dashboard')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper
