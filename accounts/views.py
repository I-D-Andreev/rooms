from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

def login_view(request, *args, **kwargs):
    return render(request, 'accounts/login.html')

def register_view(request, *args, **kwargs):
    form = UserRegistrationForm(request.POST or None)

    if form.is_valid():
        form.save()
   
    context = {'form': form}
    return render(request, 'accounts/register.html', context)