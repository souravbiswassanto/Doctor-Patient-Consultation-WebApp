from django import forms 
from .models import *

class Doctorform(forms.ModelForm):
    class Meta:
        model = Doctordata
        fields = "__all__"
        
        
# class Doctorformbeta(forms.ModelForm):
#     class Meta:
#         model = Doctordata
#         fields = ['name', 'doctoremail', 'regtype', 'regnum', 'latenightstatus', 'phonenumber', 'image',]