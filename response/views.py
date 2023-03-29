from django.shortcuts import render
from . import forms
from request.models import *
from django.shortcuts import render
from . import forms
from doctor.models import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . import forms
import pytz
from user.models import *
from doctor.models import *
import random
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import UserProfile
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from meeting import forms as meeting_form
from user import forms as user_form
from doctor import forms as doctor_form
from doctor.models import *
from meeting.models import *
from auth.models import *
from request.models import *
from meeting.models import *
from response.models import *
from request import forms as request_form
from datetime import datetime
from response import forms as res_form

def Responseaction(request):
    return render(request, 'user/home.html', context = dict)

def scheduled_meeting(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user_profile = UserProfile.objects.get(user = request.user)
    context = {}
    context['user_profile'] = user_profile
    role = user_profile.role
    data = None
    if role == "user" or role == "User":
        data = Response.objects.filter(user_profile = user_profile)
    if role == "doctor" or role == "Doctor":
        data = Response.objects.filter(doctor_profile = user_profile)
    #data = Response.objects.filter()
    datas = []
    context['role'] = role
    print (" dklajkl da lkdj lka kld alk ")
    for ds in data:
        dd = ds.patient_profile
        dd.created_at = ds.scheduled_datetime
        print (dd.created_at)
        
        if role == "user" or role == "User":
            de = Doctordata.objects.get(user_profile=ds.doctor_profile)
        if role == "Doctor" or role == "doctor":
            de = Userdata.objects.get(user_profile=ds.user_profile)
            
        lst = (dd, de, ds, ds.id)
        print (lst)
        datas.append(lst)
    
    context['resultset'] = datas 
    return render(request, 'response/responses.html', context)


def room(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    context = {}
    ptid = request.POST.get('patientfileid')
    mtid = request.POST.get('meetingfileid')
    print (ptid, mtid)
    print(type(ptid), type(mtid))
    if ptid == None or mtid == None:
        messages.error(request, 'You should enter the meetingid and patientid correctly')
        return redirect('userprofile')
    patientid = int(ptid)
    meetingid = int(mtid) 
    context['patientfileid'] = ptid
    context['meetingfileid'] = mtid 
    user_profile = UserProfile.objects.get(user = request.user)
    context['user_profile'] = user_profile
    data = None
    value = request.POST.get('firsttime')
    print ('type = ', type(value), value)
    print (value, "hellow value how are you")
    if request.method == 'POST' and not value == '1':
        form = res_form.FileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form and get the instance of the PatientFile model
            file_instance = form.save(commit=False)
            # Associate the file with the current user
            file_instance.user_profile = user_profile
            file_instance.patientid = patientid
            file_instance.meetingid = meetingid
            # Set other fields as needed
            role = user_profile.role
            file_instance.uploaded_by = role
            # Save the instance
            file_instance.save()
            messages.success(request, 'Your file has been uploaded successfully.')
            data = PatientFile.objects.filter(meetingid=meetingid, patientid=patientid)
            context['datas'] = data
            return render(request, 'response/room.html', context)
        else:
            messages.error(request, 'There was an error uploading your file.')
    else:
        form = res_form.FileForm()
        context['form'] = form
        data = PatientFile.objects.filter(meetingid=meetingid, patientid=patientid)
        context['datas'] = data
    return  render(request, 'response/room.html', context)   

def openroom(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    user_profile = UserProfile.objects.get(user = request.user)
    context = {}
    context['user_profile'] = user_profile
    return render(request, 'response/openroom.html', context)

def dltfile(request, file_id, ptid, mtid):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user_profile = UserProfile.objects.get(user = request.user)
    context = {}
    context['user_profile'] = user_profile
    obj = PatientFile.objects.get(id = int(file_id))
    
    context['patientfileid'] = ptid
    context['meetingfileid'] = mtid
    context['firsttime'] = "1"
    role = user_profile.role
    if role == "user" or role == "User":
        if obj.uploaded_by == "user":
            obj.delete()
        else:
            messages.error(request, "you don't have permission to delete this file");
    if role == "doctor" or role == "Doctor":
        if obj.uploaded_by == "doctor":
            obj.delete()
        else:
            messages.error(request, "you don't have permission to delete this file");

    data = PatientFile.objects.filter(meetingid=int(mtid), patientid=int(ptid))
    context['datas'] = data
    
    return render(request, 'response/room.html', context)