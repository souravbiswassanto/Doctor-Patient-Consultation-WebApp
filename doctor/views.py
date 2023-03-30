
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
from .models import UserProfile
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
from meeting.views import *
from request import forms as request_form
from datetime import datetime
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
from .models import UserProfile
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

from request import forms as request_form
from datetime import datetime

def home(request):
    
    print (settings.DEFAULT_IMAGE)
    doctors = Doctordata.objects.all()
    paginator = Paginator(doctors, 2) # set 10 doctors per page
    page = request.GET.get('page')
    doctors = paginator.get_page(page)
    return render(request, 'user/finalhome.html', {'doctors': doctors})

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

def profile(request):
    return render(request, 'user/home.html', context = {})

def meetinglist(request):
    return render(request, 'user/home.html', context = {})

def meetingdetails(request, meetingid):
    return render(request, 'user/home.html', context = {})

def doctor_accepted(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    if user_profile is not None:
        user_profile.last_seen = timezone.now()
        user_profile.save()
    data = Emgergency.objects.filter(doctor_profile = user_profile, status='Accepted')
    datas = []
    for ds in data:
        lst = []
        dd = ds.patient_profile
        dd.created_at = ds.reqdatetime
        print (dd.created_at)
        lst.append(dd)
        user_data = Userdata.objects.get(user_profile=ds.user_profile)
        
        lst.append(user_data)
        datas.append(lst)
    
    context['resultset'] = datas
    return render(request, 'doctor/accepted.html', context)

def doctor_pending(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    print('ei jaigai ki asche?')
    
    print('hoi aschilo')
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    patientlist = []
    if user_profile is not None:
        user_profile.last_seen = timezone.now()
        user_profile.save()
    
    data = Emgergency.objects.filter(doctor_profile=user_profile, status='Pending')
    datas = []
    for ds in data:
        
        patient_profile = ds.patient_profile
        patient_profile.created_at = ds.reqdatetime
        patient_profile.dignosis = ds.description
        print (patient_profile.created_at)
        user_data = Userdata.objects.get(user_profile=ds.user_profile)
        user_data.monthly_income = ds.id
        print ("hoboodjdo", user_data.id)
        print ("hoboodjdo", user_data.user_profile)
        lst = (patient_profile, user_data)
        datas.append(lst)
    if datas is None:
        lst = (None, None)
        datas.append(None, None)
    context['resultset'] = datas
    return render(request, 'doctor/pending.html', context)

def doctor_declined(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    if user_profile is not None:
        user_profile.last_seen = timezone.now()
        user_profile.save()
    data = Emgergency.objects.filter(doctor_profile = user_profile, status='Declined')
    datas = []
    for ds in data:
        lst = []
        dd = ds.patient_profile
        dd.created_at = ds.reqdatetime
        print (dd.created_at)
        lst.append(dd)
        user_data = Userdata.objects.get(user_profile=ds.user_profile)
        
        lst.append(user_data)
        datas.append(lst)
    
    context['resultset'] = datas
    return render(request, 'doctor/declined.html', context)


def decline_patient(request, dec_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    emgreqobj = Emgergency.objects.get(id = dec_id)
    print (emgreqobj.status)
    emgreqobj.status = "Declined"
    emgreqobj.save()
    return redirect('doctor_pending')
    
        