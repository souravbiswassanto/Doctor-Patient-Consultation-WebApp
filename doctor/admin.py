from django.contrib import admin
from .models import *
# Register your models here.


class DoctordataAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Doctordata, DoctordataAdmin)