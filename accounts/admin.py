from django.contrib import admin

from accounts.models import Profile, RegistrationLink

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(RegistrationLink)
