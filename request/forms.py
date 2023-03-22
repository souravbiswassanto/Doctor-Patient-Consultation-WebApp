from django import forms
from request.models import *

class Regreqform(forms.ModelForm):
    class Meta:
        model = Regular
        fields = "__all__"
        
class Emgreqform(forms.ModelForm):
    class Meta:
        model = Emgergency
        exclude = ['user_profile', 'doctor_profile', 'patient_profile', 'reqdatetime']

class Latereqfrom(forms.ModelForm):
    class Meta:
        model = Latenight
        fields = "__all__"