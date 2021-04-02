from django.contrib import admin

from accounts.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Profile, ProfileAdmin)
