from django import forms 
from .models import *

class FileForm(forms.ModelForm):
    class Meta:
        model = PatientFile
        exclude = ['user_profile', 'patientid', 'meetingid', 'uploaded_by']