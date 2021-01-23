from django.core.serializers.json import DjangoJSONEncoder
from room_manager.models import Meeting
import json

class MeetingEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Meeting):
            json_meeting = {
                'creator': obj.creator,
                'name': obj.name,
                'start_date': obj.start_date,
                'start_time': obj.start_time,
                'end_time': obj.end_time(),
            }

            return json.dumps(json_meeting)

        return super().default(obj)

       
