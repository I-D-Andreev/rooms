from accounts.decorators import admin_only
from django.contrib.auth.decorators import login_required
from room_manager.meeting_distance_types import MeetingDistanceTypes
from django.shortcuts import redirect, render
from django.urls import reverse
from accounts.forms import UserRegistrationForm
from django.contrib import messages
from accounts.user_types import UserTypes
from .room_forms import DeleteRoomForm, EditRoomForm
from .admin_forms import DeleteBuildingForm, DeleteUserForm, CreateBuildingForm, ChooseBuildingForm, \
                         EditBuildingForm, EditFloorForm, NearbyBuildingsForm, MeetingRoomDistanceForm, WorkingHoursForm, \
                         CreateRegistrationLinkForm, TriggerForgottenPasswordForm, DeleteAdminConfirmationForm
from .models import SystemConstants
from .location_models import Building
from accounts.models import Profile
from .mail_sender import MailSender


@login_required(login_url='login')
@admin_only
def create_room_view(request, *args, **kwargs):
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        edited_request = request.POST.copy()
        edited_request.update({'type': UserTypes.room})

        form = UserRegistrationForm(edited_request)

        if form.is_valid():
            form.save()
            messages.success(request,
            f"Room \"{form.cleaned_data['username']}\" created successfully! Please go to <a href=\"{reverse('edit_room')}\"><b>Edit a Room</b></a> to assign its location!")

            # clean the form
            form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'room_manager/admin/create_room.html', context)


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@admin_only
def edit_building_view(request, *args, **kwargs):
    form = EditBuildingForm()

    if request.method == 'POST':
        form = EditBuildingForm(request.POST)

        res = False
        if form.is_valid():
            res = form.update_fields()

        if res:
            messages.success(request, "Information updated successfully!")
        else:
            messages.error(request, "Failed to update building information!")

    context = {'form': form}
    return render(request, 'room_manager/admin/edit_building.html', context)


@login_required(login_url='login')
@admin_only
def delete_building_view(request, *args, **kwargs):
    form = DeleteBuildingForm()

    if request.method == 'POST':
        form = DeleteBuildingForm(request.POST)
        res = False

        if form.is_valid():
            res = form.delete_building()
        
        if res:
            messages.success(request, "Building deleted successfully!")
            form = DeleteBuildingForm()
        else:
            messages.error(request, "Failed to delete building!")

    context = {'form': form}
    return render(request, 'room_manager/admin/delete_building.html', context)


@login_required(login_url='login')
@admin_only
def edit_floor_view(request, *args, **kwargs):
    form = EditFloorForm()
    
    if request.method == 'POST':
        form = EditFloorForm(request.POST)

        res = False
        if form.is_valid():
            res = form.update_fields()

        if res:
            messages.success(request, "Information updated successfully!")
        else:
            messages.error(request, "Failed to update floor information!")

    context = {'form' : form}
    return render(request, 'room_manager/admin/edit_floor.html', context)


@login_required(login_url='login')
@admin_only
def configure_floors_view(request, *args, **kwargs):
    form = ChooseBuildingForm()
    context = {'form': form}
    return render(request, 'room_manager/admin/configure_floors.html', context)



@login_required(login_url='login')
@admin_only
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
    shouldInfer = SystemConstants.get_constants().infer_nearby_buildings

    nearby_buildings = Building.all_nearby_building_pairs_list(shouldInfer)
    context = {'nearby_buildings': nearby_buildings, 'shouldInfer': shouldInfer, 'form': form}
    return render(request, 'room_manager/admin/near_buildings.html', context)



@login_required(login_url='login')
@admin_only
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
    context = {'meeting_form': meeting_form, 'working_hours_form' : working_hours,
        'number_floors': MeetingDistanceTypes.number_floors,
        'near_buildings': MeetingDistanceTypes.near_buildings }
    return render(request, 'room_manager/admin/system_constants.html', context)


@login_required(login_url='login')
@admin_only
def delete_user_view(request, *args, **kwargs):
    form = DeleteUserForm()

    if request.method == 'POST':
        form = DeleteUserForm(request.POST)

        res = False
        if form.is_valid():
            res = form.delete_user()

        if res:
            messages.success(request, "User deleted successfully!")
        else:
            messages.error(request, "Failed to delete user!")

    context = {'form': form}
    return render(request, 'room_manager/admin/delete_user.html', context)


@login_required(login_url='login')
@admin_only
def delete_room_view(request, *args, **kwargs):
    form = DeleteRoomForm()

    if request.method == 'POST':
        form = DeleteRoomForm(request.POST)

        res = False
        if form.is_valid():
            res, message = form.delete_room()

        if res:
            messages.success(request, message)
        else:
            messages.error(request, message)

    context = {'form': form}
    return render(request, 'room_manager/admin/delete_room.html', context)


@login_required(login_url='login')
@admin_only
def trigger_forgotten_password_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = TriggerForgottenPasswordForm(data=request.POST, user=request.user)

        if form.is_valid():
            link = form.create_link()

            if link:
                return use_forgotten_password_link(request, link)
            else:
                messages.error(request, "Failed to trigger password reset!")


    form = TriggerForgottenPasswordForm(user=request.user)
    account_types = form.get_account_types()
   
    context = {'form': form, 'accounts': account_types}
    return render(request, 'room_manager/admin/trigger_forgotten_pass.html', context)


@login_required(login_url='login')
@admin_only
def create_registration_link_view(request, *args, **kwargs):
    form = CreateRegistrationLinkForm()

    if request.method == 'POST':
        form = CreateRegistrationLinkForm(request.POST)
        link = form.create_link()
        
        if link:
            return use_registration_link(request, link, form.get_email())
        else:
            messages.error(request, "Failed to create registration link!")

    context = {'form': form}
    return render(request, 'room_manager/admin/registration_link.html', context)


@login_required(login_url='login')
@admin_only
def delete_admin_view(request, *args, **kwargs):
    form = DeleteAdminConfirmationForm(user=request.user)

    if request.method == 'POST':
        form = DeleteAdminConfirmationForm(user=request.user, data=request.POST)

        res = False
        if form.is_valid():
            res = form.try_delete()
        
        if res:
            return redirect('login')
        else:
            messages.error(request, "Failed to delete account!")


    context = {'form': form, 'num_admins': Profile.objects.filter(type__exact=UserTypes.admin).count()}
    return render(request, 'room_manager/admin/delete_admin.html', context)




#  ---------------------- Helpers ----------------------

# Helper function. After the registration link is created
# send an email (if email is provided) and redirect to success page.
def use_registration_link(request, link, email):
    full_url_path = link.get_full_url(request)
    
    shouldSendEmail = False
    emailSent = False

    if email:
        shouldSendEmail = True
        emailSent = MailSender.send_mail(
            MailSender.create_send_registration_link_title(request.user),
            MailSender.create_send_registration_link_message(link, full_url_path),
            email)
    

    context = {'link': link, 'full_url': full_url_path, 'shouldSendEmail': shouldSendEmail, 'emailSent': emailSent, 'email': email}
    return render(request, 'room_manager/admin/registration_link_success.html', context)



def use_forgotten_password_link(request, link):
    full_url_path = link.get_full_url(request)
    email = link.profile.user.email
    emailSent = MailSender.send_mail(
            MailSender.create_forgotten_password_title(request.user),
            MailSender.create_forgotten_password_message(link, full_url_path),
            email)
    context = {'link': link, 'email': email, 'emailSent': emailSent}
    return render(request, 'room_manager/admin/trigger_forgotten_pass_success.html', context)
