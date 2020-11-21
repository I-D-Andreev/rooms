from django.shortcuts import redirect

def unauthenticated_user_only(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper