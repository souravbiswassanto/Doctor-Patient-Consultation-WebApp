from django.contrib import admin
from .models import *
#Register your models here.
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'doctor_profile', 'patient_profile',]
admin.site.register(Response, ResponseAdmin)

class PatientFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_profile', 'patientid','meetingid','filename']
admin.site.register(PatientFile, PatientFileAdmin)