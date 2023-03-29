from django.contrib import admin
from .models import *
# Register your models here.


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'name', 'dob', 'occupation', 'monthly_income', 'address', 'NID', 'image',]

admin.site.register(Userdata, UserDataAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'role', 'otp_verified']

admin.site.register(UserProfile, UserProfileAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender']

admin.site.register(Patient, PatientAdmin)