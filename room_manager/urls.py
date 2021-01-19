"""draw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from room_manager.views import *


urlpatterns = [
    path('', RedirectView.as_view(pattern_name="login")),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('dashboard/create-room', create_room_view, name="create_room"),
    path('dashboard/cancel-booking', cancel_booking_view, name="cancel_booking"),
    path('dashboard/book-room', book_room_view, name="book_room"),
    path('dashboard/statistics', statistics_view, name="statistics"),

]
