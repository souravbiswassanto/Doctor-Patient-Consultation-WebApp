from django.db import models
# Create your models here.
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError

class Userdata(models.Model):
    
    gender_choice = (
            ('female', 'Female'),
            ('male', 'Male'),
            ('other', 'Other'),
        )
    
    userid = models.AutoField
    name = models.CharField(max_length = 190, null = True, blank = True)
    dob = models.DateField(null = True)
    occupation = models.CharField(max_length = 200, null = True)
    monthly_income = models.IntegerField(null = True)
    address = models.CharField(max_length = 300, null = True)
    NID = models.CharField(max_length = 20, unique = True, null = True)
    image = models.ImageField(upload_to="images/",  blank=True)
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    
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

class Patient(models.Model):
    gender_choice = (
            ('female', 'Female'),
            ('male', 'Male'),
            ('other', 'Other'),
        )
    patientid = models.AutoField
    userid = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    diagnosis = models.TextField(blank = True, null = True)
    name = models.CharField(max_length= 30, blank = True, null = True)
    age = models.IntegerField(blank = True, null = True)
    dob = models.DateField(blank = True, null = True)
    gender = models.CharField(max_length=30, blank=True, null=True, choices=gender_choice)
    
    def __str__(self):
        return self.name
    
class Review(models.Model):
    reviewid = models.AutoField
    userid = models.ForeignKey(Userdata, on_delete=models.CASCADE)
    doctorid = models.CharField(max_length= 20, blank = True, null = True)
    rating = models.IntegerField(blank = True, null = True)
    feedback = models.TextField(blank = True, null = True)