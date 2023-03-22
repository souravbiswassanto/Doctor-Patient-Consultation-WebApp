from django.contrib import admin
from .models import *
#Register your models here.
class RequestdataAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'doctor_profile', 'patient_profile', 'reqdatetime']
admin.site.register(Emgergency, RequestdataAdmin)