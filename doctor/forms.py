from django import forms 
from .models import *

class Doctorform(forms.ModelForm):
    class Meta:
        model = Doctordata
        exclude = ['user_profile']
        
        
# class Doctorformbeta(forms.ModelForm):
#     class Meta:
#         model = Doctordata
#         fields = ['name', 'doctoremail', 'regtype', 'regnum', 'latenightstatus', 'phonenumber', 'image',]


class Activedoctorform(forms.ModelForm):
    
    class Meta:
        model = Activedoctor
        fields = "__all__"
        
class Spamreportform(forms.ModelForm):
    class meta:
        model = Spamreport
        fields = "__all__"
