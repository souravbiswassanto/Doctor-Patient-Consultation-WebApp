
# Create your models here.
from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.
from user.models import *
class Doctordata(models.Model):
    
    gender_choice = (
            ('female', 'Female'),
            ('male', 'Male'),
            ('other', 'Other'),
        )
    regt = (
            ('medical', 'Medical'),
            ('dental', 'Dental'),
        )
    latenight = (
            ('yes', 'Yes'),
            ('no', 'No'),
        )
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='doctor_data', default = None)
    name = models.CharField(max_length = 200, null = True, blank = True)
    doctoremail = models.EmailField(max_length = 200, null = True, blank = True)
    regtype = models.CharField(max_length=30, blank=True, null=True, choices=regt)
    regnum = models.CharField(max_length = 30, unique = True, null = True, blank = True)
    NID = models.CharField(max_length = 20, unique = True, null = True, blank = True)
    image = models.ImageField(upload_to="images/",  blank=True, null = True)
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    dob  = models.DateField(null = True, blank = True)
    bio = models.TextField(null = True, blank = True)
    degrees = models.CharField(max_length = 200, null = True, blank = True)
    working_hospital = models.CharField(max_length = 200, null = True, blank = True)
    designation = models.CharField(max_length = 200, blank = True, null = True)
    latenightstatus = models.CharField(max_length=30, blank=True, null=True, choices=latenight)
    chamberaddress = models.CharField(max_length = 200, null = True, blank = True)
    oldpassword = models.CharField(max_length=128, null = True, blank = True)
    newpassword = models.CharField(max_length=18, null = True, blank = True)
    confirmpassword = models.CharField(max_length=18, null = True, blank = True)
    active_time_start = models.TimeField(null = True, blank = True)
    active_time_end = models.TimeField(null = True, blank = True)
    active_day = models.DateField(blank = True, null = True)
    visits = models.IntegerField(blank = True, null = True)
    rating = models.FloatField(default=0.0, blank = True, null = True)
    ratingcount = models.IntegerField(default=0, blank = True, null= True)
    def __str__(self):
        return self.name
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="70" width="60" />'.format(self.image.url))
    image_tag.short_description = 'Image'

    def imageurl(self):
        if self.image:
            return self.image.url
        else:
            return ""


class Activedoctor(models.Model):
    activeid = models.AutoField
    doctorid = models.ForeignKey(Doctordata, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.doctorid.name
    
class Spamreport(models.Model):
    reportid = models.AutoField
    doctorid = models.ForeignKey(Doctordata, on_delete=models.CASCADE)
    userid = models.CharField(max_length= 200, blank = True, null = True)
    reason = models.TextField(blank = True, null = True)
    spamcount = models.IntegerField(null = True)
    
class Blockeduser(models.Model):
    blockid = models.AutoField
    blockuserid = models.CharField(max_length = 30, null = True, blank = True)
    