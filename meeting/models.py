from django.db import models

from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError
#from doctor.models import Doctordata

# class Meetingdata(models.Model):
    
#     gender_choice = (
#             ('female', 'Female'),
#             ('male', 'Male'),
#             ('other', 'Other'),
#         )
    
#     meetingid = models.AutoField
#     meetingurl = models.CharField(max_length = 200, null = True, blank = True)
#     meetingcode = models.CharField(max_length = 200, blank = True, null = True)
#     meetingdate = models.DateField(null = True)
#     meetingpassword = models.CharField(max_length = 20, null = True, blank = True)
#     meetingheldstatus = models.CharField(max_length = 30, blank = True, null = True)
#     patientid = models.CharField(max_length = 200, null = True)
#     doctorid = models.ForeignKey(Doctordata, on_delete=models.CASCADE)
    