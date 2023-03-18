from django.contrib import admin
from .models import *
# Register your models here.


class DoctordataAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'name', 'doctoremail', 'regtype', 'regnum', 'NID', 'image', 'gender']

admin.site.register(Doctordata, DoctordataAdmin)