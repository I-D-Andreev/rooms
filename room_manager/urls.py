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
    path('dashboard/edit-building', edit_building_view, name="edit_building"),
    path('dashboard/delete-building', delete_building_view, name="delete_building"),
    path('dashboard/configure-floors', configure_floors_view, name="configure_floors"),
    path('dashboard/edit-floor', edit_floor_view, name="edit_floor"),
    path('dashboard/near-buildings', near_buildings_view, name="near_buildings"),
    path('dashboard/system-constants', system_constants_view, name="system_constants"),
    path('dashboard/delete-user', delete_user_view, name="delete_user"),
    path('dashboard/delete-room', delete_room_view, name="delete_room"),
    path('dashboard/create-registration-link', create_registration_link_view, name="registration_link"),
    path('dashboard/trigger-forgotten-password', trigger_forgotten_password_view, name="trigger_forgotten_password"),
    path('dashboard/delete-admin', delete_admin_view, name="delete_admin"),


    # user
    path('dashboard/book-room', book_room_view, name="book_room"),
    path('dashboard/cancel-booking', cancel_booking_view, name="cancel_booking"),
    path('dashboard/my-schedule', my_schedule_view, name="my_schedule"),
    path('dashboard/room-schedule', room_schedule_view, name="room_schedule"),
    path('dashboard/multi-room-schedule', multi_room_schedule_view, name="multi_room_schedule"),
    # user statistics
    path('dashboard/statistics/room-utilization', room_utilization_statistics_view, name="room_utilization_statistics"),
    path('dashboard/statistics/multi-room-utilization', multi_room_utilization_statistics_view, name="multi_room_utilization_statistics"),
    path('dashboard/statistics/busiest-hours', busiest_hours_view, name="busiest_hours_statistics"),
    path('dashboard/statistics/failed-bookings', failed_bookings_view, name="failed_bookings_statistics"),



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
    path('get-building/<int:building_id>', get_building, name="get_building"),
    path('get-floor/<int:floor_id>', get_floor, name="get_floor"),
    path('get-user-info/<int:profile_id>', get_user_info, name="get_user_info"),

]
