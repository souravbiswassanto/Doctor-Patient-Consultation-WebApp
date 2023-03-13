from django.shortcuts import render, redirect
from . import forms
from user.models import *
from doctor.models import *
import random
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate, login


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



def userhome(request):
    context = {}
    
    # check if user is authenticated
    if request.user.is_authenticated:
        # check if user has completed otp verification
        try:
            user_profile = UserProfile.objects.get(user=request.user, otp_verified=True)
            context['user_profile'] = user_profile
        except UserProfile.DoesNotExist:
            pass
    
    # check if user is registered
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        context['user_profile'] = user_profile
    except UserProfile.DoesNotExist:
        pass
    
    return render(request, 'user/finalhome.html', context)


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


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

