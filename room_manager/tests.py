from room_manager.location_models import Building, Floor
from django.contrib.auth.models import User
from accounts.user_types import UserTypes
from django.test import TestCase
from room_manager.models import Meeting
from accounts.forms import UserRegistrationForm
from datetime import datetime
import json

# Create your tests here.
class TestAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Add an admin, a user and a room
        admin = UserRegistrationForm(data=
                    {'username': 'admin_1', 'email': 'h@h.com', 'password1': 'das123ads1@a1',
                    'password2': 'das123ads1@a1', 'capacity': 0,'type': UserTypes.admin
                    }).save()

        user = UserRegistrationForm(data=
                        {'username': 'user_1', 'email': 'uh@h.com', 'password1': 'das123ads1@a1',
                        'password2': 'das123ads1@a1', 'capacity': 0,'type': UserTypes.user
                        }).save()
           
        room = UserRegistrationForm(data=
                    {'username': 'room_1', 'email': 'h@h.com', 'password1': 'das123ads1@a1',
                    'password2': 'das123ads1@a1', 'capacity': 5,'type': UserTypes.room
                    }).save()
        
  
        building = Building.objects.create(name="building_1")
        floor1 = Floor.objects.create(building=building, name="floor_1", actual_floor=0)
        floor2 = Floor.objects.create(building=building, name="floor_2", actual_floor=1)
        floor3 = Floor.objects.create(building=building, name="floor_3", actual_floor=2)

        admin.profile.floor = floor1
        admin.profile.save()

        user.profile.floor = floor2
        user.profile.save()

        room.profile.floor = floor3
        room.profile.save()

        today = datetime.now().astimezone().replace(microsecond=0)
        Meeting.objects.create(name="meeting_1", creator=user.profile, room=room.profile,
            start_date=today.date(), start_time=today.time(), duration=30, participants_count=2)


    @staticmethod
    def get_admin():
        return User.objects.get(username="admin_1")

    @staticmethod
    def get_user():
        return User.objects.get(username="user_1")

    @staticmethod
    def get_room():
        return User.objects.get(username="room_1")

    @staticmethod
    def get_floor1():
        return Floor.objects.get(name="floor_1")
    
    @staticmethod
    def get_building():
        return Building.objects.get(name="building_1")

    @staticmethod
    def get_meeting():
        return Meeting.objects.get(name="meeting_1")


    def test_get_user_info(self):
        non_user = TestAPI.get_admin()
        user = TestAPI.get_user()

        resp = self.client.get(f'/get-user-info/{non_user.profile.id}')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(f'/get-user-info/{user.profile.id}')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'username': user.username,
                'public_name': user.profile.public_name,
                'email': user.email,
                'building_id': user.profile.floor.building.id,
                'floor_id': user.profile.floor.id
            })


    def test_get_floor(self):
        floor = TestAPI.get_floor1()

        resp = self.client.get(f'/get-floor/300')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(f'/get-floor/{floor.id}')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'name': floor.name
            }
        )


    def test_get_room(self):
        room = TestAPI.get_room()

        resp = self.client.get(f'/get-room/300')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(f'/get-room/{room.profile.id}')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'id': room.profile.id,
                'username': room.username,
                'public_name': room.profile.public_name,
                'email': room.email,
                'capacity': room.profile.capacity,
                'floorId': room.profile.floor.id,
                'buildingId': room.profile.floor.building.id
            }
        )


    def test_get_meeting(self):
        meeting = TestAPI.get_meeting()

        resp = self.client.get(f'/get-meeting/300')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'id' : '',
                'room' : '',
                'start_date' : '',
                'start_time' : '',
                'duration': '',
                'participants_count': '',
            }
        )

        resp = self.client.get(f'/get-meeting/{meeting.id}')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'id' : meeting.id,
                'room' : meeting.room.public_name,
                'start_date' : str(meeting.start_date),
                'start_time' : str(meeting.start_time),
                'duration': meeting.duration,
                'participants_count': meeting.participants_count,
            }
        )
    

    def test_get_meeting_creator(self):
        meeting = TestAPI.get_meeting()

        resp = self.client.get(f'/get-meeting-creator/300')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(f'/get-meeting-creator/{meeting.id}')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'meeting_id': meeting.id,
                'creator_user_id': meeting.creator.user.id,
                'creator_username': meeting.creator.user.username,
                'account_type': meeting.creator.type
            }
        )
        

    def test_get_building(self):
        building = TestAPI.get_building()

        resp = self.client.get(f'/get-building/300')
        self.assertEqual(resp.status_code, 404)

        resp = self.client.get(f'/get-building/{building.id}')
        self.assertJSONEqual(
            str(resp.content, encoding='utf-8'),
            {
                'name': building.name,
                'description': building.description
            }
        )


    def test_get_building_floors(self):
        building = TestAPI.get_building()

        resp = self.client.get(f'/get-building-floors/300')
        self.assertEqual(str(resp.content, encoding='utf-8'), '[]')

        resp = self.client.get(f'/get-building-floors/{building.id}')
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), 
        [{
            'id': floor.id,
            'name': floor.name,
            'actual_floor': floor.actual_floor,
            'full_name': str(floor)
        } for floor in building.floors.order_by('actual_floor')])


    def test_get_all_building_floors(self):
        resp = self.client.get(f'/get-building-floors')
        self.assertJSONEqual(str(resp.content, encoding='utf-8'), 
        [{
            'id': floor.id,
            'name': floor.name,
            'actual_floor': floor.actual_floor,
            'full_name': str(floor)
        } for floor in Floor.objects.all()])


    def test_get_room_schedule(self):
        room = TestAPI.get_room()
        meeting = TestAPI.get_meeting()

        resp = self.client.get('/get-room-schedule/300')
        self.assertEqual(str(resp.content, encoding='utf-8'), '[]')

        resp = self.client.get(f'/get-room-schedule/{room.id}')
        output = json.loads(str(resp.content, encoding='utf-8'))

        self.assertFalse(output['is_room_free'])
        self.assertTrue(meeting.name in [m['name'] for m in output['meetings']])


    def test_delete_near_building_pair(self):
        resp = self.client.delete('/near-buildings-pair/100/200')
        self.assertEqual(resp.status_code, 404)

        building1 = TestAPI.get_building()
        building2 = Building.objects.create(name="building_2")

        building1.close_buildings.add(building2)
        self.assertTrue(building1 in building2.close_buildings.all())
        self.assertTrue(building2 in building1.close_buildings.all())

        resp = self.client.delete(f'/near-buildings-pair/{building1.id}/{building2.id}')
        
        building1.refresh_from_db()
        building2.refresh_from_db()
        self.assertFalse(building1 in building2.close_buildings.all())
        self.assertFalse(building2 in building1.close_buildings.all())


    def test_save_building_floors(self):
        resp = self.client.post(f'/save-building-floors/300')
        self.assertEqual(resp.status_code, 404)

        other_building = Building.objects.create(name="other123")
        
        floor_names = ['fl1', 'fl2', 'fl3']
        resp = self.client.post(f'/save-building-floors/{other_building.id}',
            data={'floors[]': floor_names})
        
        other_building.refresh_from_db()
       
        for idx, floor_name in enumerate(floor_names):
            other_building_floor = other_building.floors.all().filter(actual_floor=idx).first()
            self.assertTrue(other_building_floor is not None)
            self.assertEqual(floor_name, other_building_floor.name)