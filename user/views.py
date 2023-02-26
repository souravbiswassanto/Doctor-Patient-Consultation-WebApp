from django.shortcuts import render
from . import forms
from user.models import *
from doctor.models import *
import random
from django.http import JsonResponse

def doctor_detail(request, doctor_id):
    doctor = doctor.objects.get(id=doctor_id)

    # update activetime here, for example:
    doctor.activetime += 3660 # add 1 minute

    doctor_data = {
        'id': doctor.id,
        'name': doctor.name,
        'activetime': doctor.activetime,
        # add any other doctor data you need
    }

    # return doctor data as a JSON response
    return JsonResponse(doctor_data)


def home(request):
    Usertable = Userdata.objects.all()
    dict = {
        'User' : Usertable, 'Range' : 4,    
    }
    return render(request, 'user/index.html', context = dict)

def form(request):
    Userform = forms.Userform
    
    dict = {
        'User' : Userform,
    }
    
    if request.method == "POST":
        Userdata = forms.Userform(request.POST, request.FILES)
        if Userdata.is_valid():
            Userdata.save(commit=True)
            return home(request)
    return render(request, 'user/form.html', context=dict)

def createpatient(request):
    Doctor = Doctordata.objects.all()
    
    dict = {
        'Doctor' : Doctor,
    }
    if (request.method == "POST"):
        patient = forms.Userform(request.POST);
        if patient.is_valid():
            patient.save(commit= True)  
            return home(request)
    return render(request, 'user/home.html', context = dict)

def profile(request):
    return render(request, 'user/home.html', context = dict)

def showpatients(request):
    return render(request, 'user/home.html', context = dict)

def showpatients(request):
    return render(request, 'user/home.html', context = dict)

