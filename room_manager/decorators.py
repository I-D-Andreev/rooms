from accounts.user_types import UserTypes
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied


def user_only(view_function):
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.profile.type == UserTypes.user:
                return view_function(request, *args, **kwargs)
        except ObjectDoesNotExist:
            pass

        raise PermissionDenied()  # 403 Forbidden page

    return wrapper
