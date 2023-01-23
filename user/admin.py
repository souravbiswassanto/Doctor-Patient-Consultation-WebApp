from django.contrib import admin
from .models import *
# Register your models here.


class UserdataAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

admin.site.register(Userdata, UserdataAdmin)