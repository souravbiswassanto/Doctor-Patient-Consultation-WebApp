from django import forms
from .models import *

class Userform(forms.ModelForm):
    class Meta:
        model = Userdata
        fields = "__all__"
        
        