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

class UserProfileManager(UserManager):
    def create_user_profile(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a UserProfile with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser_profile(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a UserProfile with the given phone_number and password,
        and marks it as a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user_profile(phone_number, password, **extra_fields)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, region='BD')
    otp = models.CharField(max_length=6, null=True, blank=True)
    role = models.CharField(max_length=50)
    otp_verified = models.BooleanField(default= False)
    join_date = models.DateField(blank = True, null = True)
    last_seen = models.DateTimeField(blank=True, null=True)
    is_sub = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    objects = UserProfileManager()
    def __str__(self):
        return str(self.id)


class Userdata(models.Model):
    
    gender_choice = (
            ('male', 'male'),
            ('female', 'female'),
            ('other', 'other'),
        )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_data', default = None)
    name = models.CharField(max_length = 190, null = True, blank = True)
    dob = models.DateField(null = True, blank = True)
    occupation = models.CharField(max_length = 200, null = True, blank = True)
    monthly_income = models.IntegerField(null = True, blank = True)
    address = models.CharField(max_length = 300, null = True, blank = True)
    NID = models.CharField(max_length = 20, unique = True, null = True, blank = True)
    image = models.ImageField(upload_to="images/",  blank=True)
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    bio = models.TextField(null = True, blank = True)
    oldpassword = models.CharField(max_length=128, null = True, blank = True)
    newpassword = models.CharField(max_length=18, null = True, blank = True)
    confirmpassword = models.CharField(max_length=18, null = True, blank = True)
    active_time_start = models.TimeField(null = True, blank = True)
    active_time_end = models.TimeField(null = True, blank = True)
    active_day = models.DateField(blank = True, null = True)
    subscribe = models.DateField(blank = True, null = True)
    meeting_count = models.IntegerField(blank = True, null = True, default=0)
    is_sub = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user_profile)
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""

def get_current_time():
    dhaka = pytz_timezone('Asia/Dhaka')
    return timezone.now().astimezone(dhaka)

class Patient(models.Model):
    gender_choice = (
            ('female', 'Female'),
            ('male', 'Male'),
            ('other', 'Other'),
        )
    
    user_profile = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    diagnosis = models.TextField(blank = True, null = True)
    name = models.CharField(max_length= 30, blank = True, null = True)
    age = models.IntegerField(blank = True, null = True)
    #dob = models.DateField(blank = True, null = True)
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    image = models.ImageField(upload_to="images/",  blank=True, null = True)
    created_at = models.DateTimeField(default=get_current_time(), blank = True, null = True)
    def __str__(self):
        return str(self.id)
    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.instance.user_profile = user_profile
            
class Review(models.Model):
    reviewid = models.AutoField
    userid = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    doctorid = models.CharField(max_length= 20, blank = True, null = True)
    rating = models.IntegerField(blank = True, null = True)
    feedback = models.TextField(blank = True, null = True)