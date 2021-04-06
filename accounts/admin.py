from django.contrib import admin

from accounts.models import Profile, RegistrationLink, ForgottenPasswordLink

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(RegistrationLink)
admin.site.register(ForgottenPasswordLink)
