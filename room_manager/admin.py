from django.contrib import admin

from room_manager.models import Meeting

class MeetingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Meeting, MeetingAdmin)
