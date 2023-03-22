
# Create your models here.
from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError
from user.models import *
from doctor.models import *




class Regular(models.Model):
    
    regularid = models.AutoField
    userid = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    doctorid = models.ForeignKey(Doctordata, on_delete=models.CASCADE)
    patientid = models.CharField(max_length = 200, null = True)
    reqdate = models.DateField(null = True)

class Emgergency(models.Model):
    reqstat = (
            ('declined', 'Declined'),
            ('accepted', 'Accepted'),
            ('pending', 'Pending'),
        )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_data_req', blank = True, null = True)
    doctor_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='doctor_data_req', blank = True, null = True)
    patient_profile = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_data', blank = True, null = True)
    description = models.TextField(blank = True, null = True)
    reqdatetime = models.DateTimeField(null = True, blank = True)
    status = models.CharField(max_length= 30, blank = True, null = True,default = "Pending")
    
class Latenight(models.Model):
    reqstat = (
            ('declined', 'Declined'),
            ('accepted', 'Accepted'),
            ('pending', 'Pending'),
        )
    latenightid = models.AutoField
    userid = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    doctorid = models.ForeignKey(Doctordata, on_delete=models.CASCADE)
    patientid = models.CharField(max_length = 200, null = True)
    reqdate = models.DateField(null = True)
    status = models.CharField(max_length= 30, blank = True, null = True, choices = reqstat, default = "Pending")
 