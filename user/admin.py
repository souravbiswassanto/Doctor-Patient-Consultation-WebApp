from django.contrib import admin
from .models import *
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

admin.site.register(Userdata, UserProfileAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'role']

admin.site.register(UserProfile, UserProfileAdmin)