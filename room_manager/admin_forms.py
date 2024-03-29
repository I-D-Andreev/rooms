from django import forms
from django.contrib.auth import authenticate
from .meeting_distance_types import MeetingDistanceTypes
from .models import SystemConstants
from .location_models import Building, Floor
from accounts.models import Profile, RegistrationLink, ForgottenPasswordLink
from accounts.user_types import UserTypes

class CreateBuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'description']
        labels = {
            'name': 'Building Name',
            'description': 'Description (optional)'
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'style': 'resize:none'})
        }


# Bind a Select element to display all the floors of a building
class ChooseBuildingForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='')


class EditBuildingForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='', label="Choose a Building")
    name = forms.CharField(max_length=150, label="Building Name")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'style': 'resize:none'}), label="Description (optional)", required=False)

    def update_fields(self):
        if self.is_valid():
            try:
                cleaned_data = self.cleaned_data
                building = cleaned_data["building"]
                building.name = cleaned_data["name"]
                building.description = cleaned_data["description"]
                building.save()

                return True
            except Exception as ex:
                print(f"Exception: {ex}")

        return False


class DeleteBuildingForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='', label="Choose a Building")
    
    # used only to display data 
    name = forms.CharField(max_length=150, label="Building Name", required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'style': 'resize:none'}), label="Description (optional)", required=False)

    def delete_building(self):
        if self.is_valid():
            try:
                building = self.cleaned_data["building"]
                building.delete()
                return True
            except Exception as ex:
                print(f"Exception: {ex}")
        
        return False


class EditFloorForm(forms.Form):
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='', label="Choose a Floor")
    name = forms.CharField(max_length=150, label="Floor Name")

    def update_fields(self):
        if self.is_valid():
            try:
                cleaned_data = self.cleaned_data
                floor = cleaned_data["floor"]
                name = cleaned_data["name"]

                current_floor_names = [floor.name for floor in floor.building.floors.all()]

                if name not in current_floor_names:
                    floor.name = name
                    floor.save()
                    return True, "Information updated successfully!"
                else:
                    return False, "Failed to update floor information! Floor with such a name already exists!"

            except Exception as ex:
                print(ex)

        return False, "Failed to update floor information!"


class MeetingRoomDistanceForm(forms.Form):
    type = forms.CharField(widget=forms.Select(choices=MeetingDistanceTypes.as_choice_list()))
    floors = forms.IntegerField(min_value=0, required=True)
    infer_nearby_buildings = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        constants = SystemConstants.get_constants()
        self.fields['type'].initial = constants.distance_type
        self.fields['floors'].initial = constants.distance_floors
        self.fields['infer_nearby_buildings'].initial = constants.infer_nearby_buildings


    def update_data(self):
        if self.is_valid():
            try:
                cleaned_type = self.cleaned_data['type']
                cleaned_floors = int(self.cleaned_data['floors'])
                cleaned_infer = self.cleaned_data['infer_nearby_buildings']

                SystemConstants.update_meeting_room_distance_constants(cleaned_type, cleaned_floors, cleaned_infer) 
                return True
            except Exception as e:
                print(e)

        return False



class WorkingHoursForm(forms.Form):
    start_work_hour = forms.IntegerField(min_value=0, max_value=23, label='Start hour:')
    start_work_minute = forms.IntegerField(min_value=0, max_value=59, label='Start minute:')

    end_work_hour = forms.IntegerField(min_value=0, max_value=23, label='End hour:')
    end_work_minute = forms.IntegerField(min_value=0, max_value=59, label='End minute:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        constants = SystemConstants.get_constants()
        self.fields['start_work_hour'].initial = constants.start_work_time.hour
        self.fields['start_work_minute'].initial = constants.start_work_time.minute

        self.fields['end_work_hour'].initial = constants.end_work_time.hour
        self.fields['end_work_minute'].initial = constants.end_work_time.minute


    def update_data(self):
        if self.is_valid():
            try:
                start_hour = self.cleaned_data['start_work_hour']
                start_minute = int(self.cleaned_data['start_work_minute'])
                
                end_hour = self.cleaned_data['end_work_hour']
                end_minute = int(self.cleaned_data['end_work_minute'])

                SystemConstants.update_working_hours(start_hour, start_minute, end_hour, end_minute)
                return True
            except Exception as e:
                print(e)

        return False



class NearbyBuildingsForm(forms.Form):
    building1 = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='', required=True)
    building2 = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='', required=True)

    def add_near_buildings_pair(self):
        if self.is_valid():
            try:
                building1 = self.cleaned_data['building1']
                building2 = self.cleaned_data['building2']
                
                if building1.id == building2.id:
                    return False, "A building can't be paired with itself!"


                if (building1 in building2.close_buildings.all()) or \
                    (building2 in building1.close_buildings.all()):
                    return False, f'Building pair "{building1.name} - {building2.name}" already exists!'
                
                building1.close_buildings.add(building2)

                return True, 'Successfully added the building pair!'
            except Exception as e:
                print(e)
        
        return False, 'Failed to add the building pair!'


class DeleteUserForm(forms.Form):
    profile = forms.ModelChoiceField(queryset=Profile.objects.filter(type__exact=UserTypes.user), empty_label="", label="Choose a User")
    username = forms.CharField(required=False)
    public_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    building = forms.ModelChoiceField(queryset=Building.objects.all(), empty_label='All Buildings', label='Building', required=False)
    floor = forms.ModelChoiceField(queryset=Floor.objects.all(), empty_label='', label='Location', required=False)

    def delete_user(self):
        if self.is_valid():
            try:
                profile = self.cleaned_data["profile"]

                if profile.type != UserTypes.user:
                    return False
                
                profile.user.delete()

                return True
            except Exception as e:
                print(e)
        
        return False


class CreateRegistrationLinkForm(forms.Form):
    type = forms.CharField(widget=forms.Select(choices=UserTypes.user_admin_choice_list()), label="Registration Type")
    email = forms.EmailField(required=False, label="Email (optional)")
    link_duration = forms.IntegerField(min_value=0, label="Link Duration (minutes)", initial=30)

    def create_link(self):
        if self.is_valid():
            try:
                cleaned_data = self.cleaned_data
                type = cleaned_data["type"]
                link_duration = cleaned_data["link_duration"]

                return RegistrationLink.create_registration_link(type, link_duration)
            except Exception as e:
                print(e)
        
        return None


    def get_email(self):
        if self.is_valid():
            try:
                return self.cleaned_data["email"]
            except Exception as e:
                print(e)
        
        return None


class TriggerForgottenPasswordForm(forms.Form):
    type = forms.CharField(widget=forms.Select(choices=([("all", "All Account Types")] + UserTypes.as_choice_list())), label="Account Type", required=False)
    account = forms.ModelChoiceField(queryset=Profile.objects.all())
    username = forms.CharField(required=False, label="Username")
    name = forms.CharField(required=False, label="Name")
    email = forms.CharField(required=False, label="Email")
    link_duration = forms.IntegerField(min_value=0, label="Link Duration (minutes)", initial=120)


    def __init__(self, user, *args, **kwargs):
        self.user_profile = user.profile
        super().__init__(*args, **kwargs)

        self.fields['account'].queryset = Profile.objects.all().exclude(pk=self.user_profile.id)

    
    def create_link(self):
        if self.is_valid():
            try:
                cleaned_data = self.cleaned_data
                
                profile = cleaned_data["account"]
                link_duration = cleaned_data["link_duration"]

                return ForgottenPasswordLink.create_forgotten_password_link(profile, link_duration)
            except Exception as e:
                print(e)
        
        return None



    def get_account_types(self):
        all = Profile.objects.all().exclude(pk=self.user_profile.id)
        admins = all.filter(type__exact=UserTypes.admin)
        users = all.filter(type__exact=UserTypes.user)
        rooms = all.filter(type__exact=UserTypes.room)

        return {
            'all': self.__profiles_to_array_of_dicts(all),
            'admin': self.__profiles_to_array_of_dicts(admins),
            'user': self.__profiles_to_array_of_dicts(users),
            'room': self.__profiles_to_array_of_dicts(rooms),
        }


    #  ----- Helpers -----
    def __profiles_to_array_of_dicts(self, profiles):
        return [{"id": p.id, "name": p.public_name, "username": p.user.username, "email": p.user.email} for p in profiles]


class DeleteAdminConfirmationForm(forms.Form):
    username = forms.CharField(disabled=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DeleteAdminConfirmationForm, self).__init__(*args, **kwargs)

        self.admin = user
        self.fields['username'].initial = self.admin.username

    
    def try_delete(self):
        if self.is_valid():
            cleaned_data = self.cleaned_data

            username = cleaned_data['username']
            password  = cleaned_data['password']

            admin = authenticate(username=username, password=password)

            if admin and admin.profile.type == UserTypes.admin:
                admin.delete()
                return True

        return False