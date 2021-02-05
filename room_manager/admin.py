from django.contrib import admin

from room_manager.models import Meeting
from room_manager.location_models import Building, Floor

class MeetingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Meeting, MeetingAdmin)

admin.site.register(Building)
admin.site.register(Floor)
