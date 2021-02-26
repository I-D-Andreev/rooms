from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from accounts.user_types import UserTypes
from .room_manager import RoomManager
from django.http import JsonResponse
from .models import Meeting, SystemConstants
from .location_models import Building, Floor
from datetime import datetime
from django.contrib.auth.models import User
from accounts.models import Profile
from django.http import HttpResponse
import json

# --------------- Views ---------------
#  User, Admin, Room
@login_required(login_url='login')
def dashboard_view(request, *args, **kwargs):
    try:
        dashboard = request.user.profile.type
    except ObjectDoesNotExist:
        raise PermissionDenied()

    
    meetings_list = None
    if request.user.profile.type == UserTypes.user:
        meetings_list = RoomManager.get_user_meetings_list_today(request.user)
    elif request.user.profile.type == UserTypes.room:
      meetings_list = get_room_schedule_meetings_list(request.user)


    context = {'user': request.user, 'meetings_list': meetings_list}

    return render(request, f'room_manager/{dashboard}_dashboard.html', context)


# login + user only
def multi_room_schedule_view(request, *args, **kwargs):
    rooms = Profile.objects.filter(type__exact = UserTypes.room)
    multi_room_schedule_list = [(room, get_room_schedule_meetings_list(room.user)) for room in rooms]
    context = {'list': multi_room_schedule_list}
    return render(request, 'room_manager/user/multi_room_schedule.html', context)


# --------------- REST API ---------------
def near_buildings_pair(request, building_id1, building_id2, *args, **kwargs):
    building1 = Building.objects.filter(pk=building_id1).first() 
    building2 = Building.objects.filter(pk=building_id2).first() 

    if (request.method == 'DELETE') and (building_id1 is not None) and (building_id2 is not None):
        try:
            building1.close_buildings.remove(building2)

            data = "[]"
            shouldInfer = SystemConstants.get_constants().infer_nearby_buildings

            if shouldInfer:
                all_pairs = Building.all_nearby_building_pairs_list(shouldInfer)
                inferred_pair = [pair for pair in all_pairs if not pair[2]]
                data = json.dumps(
                    [{
                        'building1_name': inf_pair[0].name,
                        'building2_name': inf_pair[1].name,
                    } for inf_pair in inferred_pair])

            return HttpResponse(data, status=200, content_type="application/json")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(status=500)
    else:
        raise Http404()


def get_room(request, profile_id, *args, **kwargs):
    room = Profile.objects.filter(pk=profile_id).first()

    if (room is None) or (room.type != UserTypes.room):
        # return HttpResponse("{}", content_type="application/json")
        raise Http404
    else:
        floor = room.floor
        floorId = floor.id if floor else ''
        buildingId = floor.building.id if floor else ''
       
        return JsonResponse({
            'id': room.id,
            'public_name': room.public_name,
            'email': room.user.email,
            'capacity': room.capacity,
            'floorId': floorId,
            'buildingId': buildingId
        })


def get_meeting(request, id, *args, **kwargs):
    meeting = Meeting.objects.filter(pk=id).first()

    if meeting is not None:
        return JsonResponse({
            'id' : meeting.pk,
            'room' : meeting.room.public_name,
            'start_date' : meeting.start_date,
            'start_time' : meeting.start_time,
            'duration': meeting.duration,
            'participants_count': meeting.participants_count,
        })
    else:
        return JsonResponse({
            'id' : '',
            'room' : '',
            'start_date' : '',
            'start_time' : '',
            'duration': '',
            'participants_count': '',
        })

def get_meeting_creator(request, id, *args, **kwargs):
    meeting = Meeting.objects.filter(pk=id).first()

    if meeting is not None:
        return JsonResponse({
            'meeting_id': id,
            'creator_user_id': meeting.creator.user.id,
            'creator_username': meeting.creator.user.username,
            'account_type': meeting.creator.type
        })
    else:
        raise Http404


def get_room_schedule(request, id, *args, **kwargs):
    profile = Profile.objects.filter(pk=id).first()
 
    if profile is not None:
        meetings_list = get_room_schedule_meetings_list(profile.user)
        meetings_list_json = json.dumps(
            [{'creator': meeting.creator.public_name if meeting.creator else None,
             'name': meeting.name,
             'start_date': meeting.start_date_str(),
             'start_time': meeting.start_time_str(), 
             'end_time': meeting.end_time_str(),
             'background_colour': meeting.background_colour(),
             } for meeting in meetings_list])


        return HttpResponse(meetings_list_json, content_type="application/json")
    else:
        return HttpResponse("[]", content_type="application/json")


def get_all_building_floors(request, *args, **kwargs):
    floors = Floor.objects.all()

    if floors is not None:
        floors_list_json = json.dumps(
            [__floor_to_dict(floor) for floor in floors]
        )
        return HttpResponse(floors_list_json, content_type="application/json")
    else:
        return HttpResponse("[]", content_type="application/json")


def get_building_floors(request, id, *args, **kwargs):
    building = Building.objects.filter(pk=id).first()

    if building is not None:
        floors_list = building.floors.all().order_by('actual_floor')
        floors_list_json = json.dumps(
            [__floor_to_dict(floor) for floor in floors_list]
        )
        return HttpResponse(floors_list_json, content_type="application/json")
    else:
        return HttpResponse("[]", content_type="application/json")

def __floor_to_dict(floor: Floor):
    return {
        'id': floor.id,
        'name': floor.name,
        'actual_floor': floor.actual_floor,
        'full_name': str(floor)
    }


def save_building_floors(request, id, *args, **kwargs):
    building = Building.objects.filter(pk=id).first() 

    if (request.method == 'POST') and (building is not None):
        if request.POST.__contains__('floors[]'):
            new_floors = request.POST.getlist('floors[]')
            res = building.update_floors(new_floors)
            
            status = 200 if res else 500
            return HttpResponse(status=status)
    else:
        raise Http404()


# --------------- Helper Functions ---------------
def get_room_schedule_meetings_list(user: User) -> list:
    meetings_list = RoomManager.get_room_meeting_list_today_after_hour(user, datetime.now().time().hour)
    padded_meetings_list = __pad_with_free_meetings(meetings_list)
    return padded_meetings_list

# If there is time between meetings, insert 'ghost' meetings saying that the room is free.
def __pad_with_free_meetings(meeting_list: list) -> list:
    today = datetime.now().date()

    # Start from 00th minute of the current hour
    current_time = datetime.now().time()
    current_time = current_time.replace(hour=current_time.hour, minute=0, second=0, microsecond=0)

    current_date_time = datetime.combine(today, current_time).astimezone()
    
    
    # If we have no meetings, return only one ghost meeting until midnight.
    if len(meeting_list) == 0:      
        return [__create_ghost_meeting(today, current_time, __time_until_midnight(current_time))]


    padded_meetings_list = []

    # If the first meeting is in the future, insert a Ghost meeting before it
    if not meeting_list[0].is_currently_ongoing():
        first_meeting = meeting_list[0]
        padded_meetings_list.append(__create_ghost_meeting(today, current_time, __time_until_meeting(first_meeting, current_date_time)))


    for i in range(0, len(meeting_list)-1):
        curr_meeting = meeting_list[i]
        next_meeting = meeting_list[i+1]

        # time_between_mins = (next_meeting.start_date_time() - curr_meeting.end_date_time()).total_seconds() // 60
        time_between_mins = __time_until_meeting(next_meeting, curr_meeting.end_date_time())

        padded_meetings_list.append(curr_meeting)

        if(time_between_mins >= 1):
            padded_meetings_list.append(__create_ghost_meeting(today, curr_meeting.end_time(), time_between_mins))


    last_meeting = meeting_list[-1]
    padded_meetings_list.append(last_meeting)
    
    #  if the last meeting does not go over 24:00, append one more padded meeting
    if last_meeting.start_date_time().day == last_meeting.end_date_time().day:      
        padded_meetings_list.append(__create_ghost_meeting(today, last_meeting.end_time(), __time_until_midnight(last_meeting.end_time())))

    return padded_meetings_list

def __create_ghost_meeting(start_date: datetime.date, start_time: datetime.time, duration: int):
    room_free_text = 'Room Is Free!'
    return Meeting(creator=None, room=None, name=room_free_text, 
        start_date=start_date, start_time=start_time,
        duration=duration, participants_count=0)

def __time_until_meeting(meeting: Meeting, current_date_time: datetime):
    return (meeting.start_date_time() - current_date_time).total_seconds() // 60

def __time_until_midnight(curr_time: datetime.time):
    return 1439 - (curr_time.hour * 60 + curr_time.minute)



#  Import the Different Views categories to be rendered
from .user_statistics_views import *
from .admin_views import *
from .user_views import *
from .room_views import *