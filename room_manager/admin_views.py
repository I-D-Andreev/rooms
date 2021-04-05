from django.shortcuts import render
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from accounts.user_types import UserTypes
from .room_forms import EditRoomForm
from .admin_forms import CreateBuildingForm, ChooseBuildingForm, NearbyBuildingsForm, MeetingRoomDistanceForm, WorkingHoursForm
from .models import SystemConstants
from .location_models import Building

# login + admin only
def create_room_view(request, *args, **kwargs):
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        edited_request = request.POST.copy()
        edited_request.update({'type': UserTypes.room})

        form = UserRegistrationForm(edited_request)

        if form.is_valid():
            form.save()
            messages.success(request, f"Room \"{form.cleaned_data['username']}\" created successfully!")

            # clean the form
            form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'room_manager/admin/create_room.html', context)


# login + admin only
def edit_room_view(request, *args, **kwargs):
    form = EditRoomForm()

    if request.method == 'POST':
        form = EditRoomForm(request.POST)

        res = False
        if form.is_valid():
            res = form.update_fields()

        if res:
            messages.success(request, "Information updated successfully!")
        else:
            messages.error(request, "Failed to update room information!")


    context = {'form': form}
    return render(request, 'room_manager/admin/edit_room.html', context)


# login + admin only
def create_building_view(request, *args, **kwargs):
    form = CreateBuildingForm()

    if request.method == 'POST':
        form = CreateBuildingForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Building \"{form.cleaned_data['name']}\" createad successfully!")

            # clean the form
            form = CreateBuildingForm()


    context = {'form': form}
    return render(request, 'room_manager/admin/create_building.html', context)


# login + admin only
def edit_building_view(request, *args, **kwargs):
    choose_building = ChooseBuildingForm()
    context = {'choose_building': choose_building}
    return render(request, 'room_manager/admin/edit_building.html', context)



# login + admin only
def configure_floors_view(request, *args, **kwargs):
    form = ChooseBuildingForm()
    context = {'form': form}
    return render(request, 'room_manager/admin/configure_floors.html', context)



# login + admin only
def near_buildings_view(request, *args, **kwargs):
    
    if request.method == 'POST':
        form = NearbyBuildingsForm(request.POST)

        result = False
        message = 'Failed to add the building pair!'
        if form.is_valid():
            result, message = form.add_near_buildings_pair()
        
        if result:
            messages.success(request, message)
        else:
            messages.error(request, message)

    form = NearbyBuildingsForm()
    # todo1 change to infer_nearby_buildings_constant
    shouldInfer = SystemConstants.get_constants().infer_nearby_buildings

    nearby_buildings = Building.all_nearby_building_pairs_list(shouldInfer)
    context = {'nearby_buildings': nearby_buildings, 'shouldInfer': shouldInfer, 'form': form}
    return render(request, 'room_manager/admin/near_buildings.html', context)



# login + admin only
def system_constants_view(request, *args, **kwargs):
    if request.method == 'POST':
        result = False

        if request.POST.__contains__("type") or request.POST.__contains__("floors")\
            or request.POST.__contains__("infer_nearby_buildings"):
        
            meeting_form = MeetingRoomDistanceForm(request.POST)

            if meeting_form.is_valid():
                result = meeting_form.update_data()

        elif request.POST.__contains__("start_work_hour") or request.POST.__contains__("start_work_minute")\
            or request.POST.__contains__("end_work_hour") or request.POST.__contains__("end_work_minute"):
            
            working_hours_form = WorkingHoursForm(request.POST)

            if working_hours_form.is_valid():
                result = working_hours_form.update_data()
        
        if result:
            messages.success(request, "Successfully updated!")
        else:
            messages.error(request, "Failed to update!")

   
    meeting_form = MeetingRoomDistanceForm()
    working_hours = WorkingHoursForm()
    context = {'meeting_form': meeting_form, 'working_hours_form' : working_hours}
    return render(request, 'room_manager/admin/system_constants.html', context)