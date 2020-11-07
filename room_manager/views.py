from django.shortcuts import render

# Create your views here.
def dashboard_view(request, *args, **kwargs):
    return render(request, 'room_manager/dashboard.html')