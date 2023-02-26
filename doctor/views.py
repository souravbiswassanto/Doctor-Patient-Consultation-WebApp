
from django.shortcuts import render
from . import forms
from doctor.models import *
from django.core.paginator import Paginator


def home(request):
    
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
    return render(request, 'user/home.html', context = dict)

def meetinglist(request):
    return render(request, 'user/home.html', context = dict)

def meetingdetails(request, meetingid):
    return render(request, 'user/home.html', context = dict)
