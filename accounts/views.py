from django.shortcuts import render

# Create your views here.
def login_view(request, *args, **kwargs):
    return render(request, 'accounts/login.html')

def register_view(request, *args, **kwargs):
    return render(request, 'accounts/register.html')