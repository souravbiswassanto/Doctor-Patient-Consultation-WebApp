from django import forms
from .models import *

class Userform(forms.ModelForm):
    class Meta:
        model = Userdata
        #fields = "__all__"
        exclude = ['user_profile']
        
        
class Patientform(forms.ModelForm):
    class Meta: 
        model = Patient
        fields = "__all__"
    
class Reviewform(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"