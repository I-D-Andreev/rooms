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
    path('dashboard/edit-account', edit_account_view, name="edit_account"),

    # admin
    path('dashboard/create-room', create_room_view, name="create_room"),
    path('dashboard/edit-room', edit_room_view, name="edit_room"),
    path('dashboard/create-building', create_building_view, name="create_building"),
    path('dashboard/configure-floors', configure_floors_view, name="configure_floors"),
    path('dashboard/near-buildings', near_buildings_view, name="near_buildings"),
    path('dashboard/system-constants', system_constants_view, name="system_constants"),

    # user
    path('dashboard/book-room', book_room_view, name="book_room"),
    path('dashboard/cancel-booking', cancel_booking_view, name="cancel_booking"),
    path('dashboard/my-schedule', my_schedule_view, name="my_schedule"),
    path('dashboard/room-schedule', room_schedule_view, name="room_schedule"),
    path('dashboard/multi-room-schedule', multi_room_schedule_view, name="multi_room_schedule"),
    path('dashboard/statistics', statistics_view, name="statistics"),

    # room
    path('dashboard/book-now', book_now_view, name="book_now"),
    path('dashboard/similar-rooms', nearest_room_view, name="nearest_room"),
    path('dashboard/cancel_meeting', cancel_meeting_view, name="cancel_meeting"),

    
    # user REST api
    path('get-meeting/<int:id>', get_meeting, name="get_meeting"),
    path('get-meeting-creator/<int:id>', get_meeting_creator, name="get_meeting_creator"),
    path('get-room/<int:profile_id>', get_room, name="get_room"),
    path('get-room-schedule/<int:id>', get_room_schedule, name="get_room_schedule"),
    path('get-building-floors/<int:id>', get_building_floors, name="get_building_floors"),
    path('get-building-floors', get_all_building_floors, name="get_all_building_floors"),
    path('save-building-floors/<int:id>', save_building_floors, name="save_building_floors"),
    path('near-buildings-pair/<int:building_id1>/<int:building_id2>', near_buildings_pair, name="delete_near_building_pair"),

]
