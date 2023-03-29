from django.db import models
#from doctor.models import Doctordata
from django.db import models
# Create your models here.
import pytz

from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.contrib.auth.models import AbstractUser
from datetime import datetime

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError
from user.models import *
from doctor.models import *

class Response(models.Model):
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_data_res', blank = True, null = True)
    doctor_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='doctor_data_res', blank = True, null = True)
    patient_profile = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_data_res', blank = True, null = True)
    doctorack = models.CharField(max_length= 30, blank = True, null = True)
    join_url = models.URLField(max_length=500, blank = True, null = True)
    start_meeting_url = models.URLField(max_length=500, blank = True, null = True)
    scheduled_datetime = models.DateTimeField(blank = True, null = True)
    instructions = models.TextField(blank = True, null = True)
    meeting_duration = models.IntegerField(blank = True, null = True)
    topic = models.CharField(max_length = 100,blank = True, null = True)
    payment_status = models.TextField(max_length=150, blank = True, null = True, default = "NA")
    
class PatientFile(models.Model):
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_data_file', blank = True, null = True)
    patientid = models.IntegerField(blank = True, null = True)
    meetingid = models.IntegerField(blank = True, null = True)
    uploaded_by = models.CharField(max_length= 10, blank = True, null = True)
    pdf_file = models.FileField(upload_to='documents/', blank = True, null = True)
    filename = models.CharField(max_length=100, blank = True, null = True)