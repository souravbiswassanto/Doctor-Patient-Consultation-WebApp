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

def userhome(request):
    context = {}
    doctors = Doctordata.objects.all()
    current_time = timezone.now()
    dhaka = pytz_timezone('Asia/Dhaka')
    current_time_dhaka = current_time.astimezone(dhaka)
    doctor = []
    upcoming_doctors = []
    for data in doctors:
        print (current_time_dhaka.date(), data.active_day)
        print (current_time_dhaka.time(), data.active_time_start)
        if data.active_day == current_time_dhaka.date():
            if data.active_time_start <= current_time_dhaka.time() <= data.active_time_end:
                doctor.append(data)
    
    for data in doctors:
        if data.active_day == current_time_dhaka.date():
            if data.active_time_start >= current_time_dhaka.time() and current_time_dhaka.time() >= data.active_time_end:
                upcoming_doctors.append(data)
        if data.active_day > current_time_dhaka.date():
            upcoming_doctors.append(data)
    temp = list(doctors)
    random.shuffle(doctor)
    random.shuffle(temp)
    random.shuffle(upcoming_doctors)
    context['doctors'] = doctor
    context['alldoctors'] = temp
    context['upcoming_doctors'] = upcoming_doctors
    # check if user is authenticated
    phone_number = request.session.get('phone_number')
    print('phone number: ', phone_number)
    print(request.session)
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user, otp_verified=True)
            print (user_profile)
            context['user_profile'] = user_profile
        except UserProfile.DoesNotExist:
            pass 
    
    # check if user is registered
    # try:
    #     user_profile = UserProfile.objects.get(user=request.user)
    #     context['user_profile'] = user_profile
    # except UserProfile.DoesNotExist:
    #     pass
    
    return render(request, 'user/finalhome.html', context)

def doctor_detail(request, doctor_id):
    if request.user.is_authenticated != True or request.user == None:
        messages.error(request, 'You need to be logged in for visiting this page')
        return redirect('signin')
    
    sender_user = request.user
    sender_user_profile = UserProfile.objects.get(user = sender_user)
    doctordata = Doctordata.objects.get(id = doctor_id)
    
    doctor_user_profile = doctordata.user_profile
    
    context = {}
    context['sender_user_profile'] = sender_user_profile
    context['data'] = doctordata
    context['user_profile'] = doctordata.user_profile
    form = request_form.Emgreqform()
    context['form'] = form
    current_time = timezone.now()
    dhaka = pytz_timezone('Asia/Dhaka')
    current_time_dhaka = current_time.astimezone(dhaka)
    context['time_zone'] = current_time_dhaka
    print (current_time_dhaka.date())     
    if request.method == "POST":
        current_time = timezone.now()
        dhaka = pytz_timezone('Asia/Dhaka')
        current_time_dhaka = current_time.astimezone(dhaka)
        dataform = request_form.Emgreqform(request.POST)
        
        ptid = request.POST.get('id')
        try:
            pf = Patient.objects.get(id=ptid)
        except Patient.DoesNotExist:
            messages.error(request, "This patient doesn't exists in your patient list")
            return redirect('doctor_detail', doctor_id = doctor_id)
        
        if pf.user_profile != sender_user_profile:
            messages.error(request, "This patient doesn't exists in your patient list")
            return redirect('doctor_detail', doctor_id = doctor_id)
        
            
        if dataform.is_valid():
            data = dataform.save(commit=False)
            data.user_profile = sender_user_profile
            data.doctor_profile = doctor_user_profile
            ptid = request.POST.get('id')
            patientdata = Patient.objects.get(id = ptid)
            data.patient_profile = patientdata
            data.reqdatetime = current_time_dhaka
            data.save()
            messages.success(request, 'Your request has been sent successfully')
            
            return redirect('patient_accepted')
        else:
            messages.error(request, 'something went wrong')
            return redirect('userhome')
    return render(request, 'signin/viewprofile.html', context)

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
            return redirect('home')
    return render(request, 'user/form.html', context=dict)

def createpatient(request):
    print ('helelll ldljd dl',request.user)
    if request.user is None:
        return redirect('signin')
    context = {}
    form = user_form.Patientform()
    context['form'] = form
    user_profile = UserProfile.objects.get(user = request.user)
    context['user_profile'] = user_profile    
    if request.method == "POST":
        print ("okayy")
        form = user_form.Patientform(request.POST, request.FILES, user_profile)
        print ("okay 1")
        print ('okay 2')
        print (user_profile)
        print (form.is_valid())
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user_profile = user_profile
            patient.save()
            return redirect('showpatients')
        messages.error(request, 'Saving data is failed')
        return redirect('createpatient')
    return render(request, 'user/patient.html', context)

def profile(request):
    return render(request, 'user/home.html', context = dict)

def showpatients(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user_profile = UserProfile.objects.get(user = request.user)
    context['user_profile'] = user_profile
    patientlist = Patient.objects.filter(user_profile=user_profile).order_by('-created_at')
    context['patientlist'] = patientlist
    
    print (patientlist)
    
    if request.method == "POST":
        pt_id = int(request.POST['id']) 
        print (pt_id)
        patientobj = Patient.objects.get(id = pt_id)
        name = request.POST.get('name')
        age = request.POST.get('age')
        diagnosis = request.POST.get('diagnosis')
        patientobj.name = name
        patientobj.age = age
        patientobj.diagnosis = diagnosis
        patientobj.save();
        return render(request, 'user/patientlist.html', context)
    return render(request, 'user/patientlist.html', context)

def findin(request):
    context = {}
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user = request.user)
    else:
        user_profile = None
    context['user_profile'] = user_profile
    if request.method == "POST":
        #print (request.POST['speciality'])
        spfind = request.POST.get('speciality')
        lofind = request.POST.get('location')
        visit = request.POST.get('visit')
        date_string = request.POST.get('datef')
        dafind = None
        
        if date_string:
            try:
                dafind = datetime.strptime(date_string, '%Y-%m-%d').date()
            except ValueError:
                error_message = "Invalid date format. Please enter the date in the format 'MM-DD-YYYY'"     
                messages.error(request, error_message)
                return render(request, 'search/search.html')
    
        ds = None
        
        if lofind is not None:
            ds = Doctordata.objects.filter(chamberaddress__icontains=lofind)
        else:
            ds = Doctordata.objects.all()
        doctors = []
        for d in ds:
            print (d.name, spfind)
            if spfind == '' or d.designation == spfind:
                
                if dafind == None or d.active_day == dafind:
                    
                    if int(visit) == 0:
                        doctors.append(d)
                    elif int(visit) == 1 and d.visits < 500:
                        doctors.append(d)
                    elif int(visit) == 2 and d.visits >= 500 and d.visits <= 1000:
                        doctors.append(d)
                    elif int(visit) == 3 and d.visits > 1000 and d.visits <= 2000:
                        doctors.append(d)
                    elif int(visit) == 4 and d.visits > 2000:
                        doctors.append(d)
            print ('end')
        
        
        print(doctors)
        print(user_profile, 'kaje lagse')
        context['doctors'] = doctors
        return render(request, 'search/search.html', context)
    return render(request, 'search/search.html', context)


def delete_patient(request, pt_id):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    patient_to_delete = Patient.objects.get(id = pt_id)
    patient_to_delete.delete()
    user_profile = UserProfile.objects.get(user = request.user)
    context['user_profile'] = user_profile
    patientlist = Patient.objects.filter(user_profile=user_profile).order_by('-created_at')
    context['patientlist'] = patientlist
    
    print (patientlist)
    return render(request, 'user/patientlist.html', context)

def patient_accepted(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    
    data = Emgergency.objects.filter(user_profile=user_profile, status='Accepted')
    datas = []
    for ds in data:
        lst = []
        dd = ds.patient_profile
        dd.created_at = ds.reqdatetime
        print (dd.created_at)
        lst.append(dd)
        doctor_data = Doctordata.objects.get(user_profile=ds.doctor_profile)
        
        lst.append(doctor_data)
        datas.append(lst)
    
    context['resultset'] = datas
    return render(request, 'user/accepted.html', context)

def patient_pending(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    
    data = Emgergency.objects.filter(user_profile=user_profile, status='Pending')
    datas = []
    for ds in data:
        lst = []
        dd = ds.patient_profile
        dd.created_at = ds.reqdatetime
        print (dd.created_at)
        lst.append(dd)
        doctor_data = Doctordata.objects.get(user_profile=ds.doctor_profile)
        
        lst.append(doctor_data)
        datas.append(lst)
    
    context['resultset'] = datas
    return render(request, 'user/pending.html', context)

def patient_declined(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('signin')
    
    user_profile = UserProfile.objects.get(user=request.user)
    context['user_profile'] = user_profile
    
    data = Emgergency.objects.filter(user_profile=user_profile, status='Declined')
    datas = []
    for ds in data:
        lst = []
        dd = ds.patient_profile
        dd.created_at = ds.reqdatetime
        print (dd.created_at)
        lst.append(dd)
        doctor_data = Doctordata.objects.get(user_profile=ds.doctor_profile)
        
        lst.append(doctor_data)
        datas.append(lst)
    
    context['resultset'] = datas
    return render(request, 'user/declined.html', context)
