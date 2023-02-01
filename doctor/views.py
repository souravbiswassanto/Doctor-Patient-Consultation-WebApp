
from django.shortcuts import render
from . import forms
from doctor.models import *


def home(request):
    doctortable = Doctordata.objects.all()
    dict = {
        'doctor' : doctortable,
        }
    return render(request, 'doctor/index.html', context = dict)

def form(request):
    doctordemoform = forms.Doctorform
    dict = {
        'doctor' : doctordemoform
    }
    
    if request.method == "POST":
        doctordemoform = forms.Doctorform(request.POST, request.FILES)
        
        if doctordemoform.is_valid():
            doctordemoform.save(commit = True)
            return home(request)
        
    return render(request, 'doctor/form.html', context = dict)