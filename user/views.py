from django.shortcuts import render
from . import forms
from user.models import *


def home(request):
    Usertable = Userdata.objects.all()
    dict = {
        'User' : Usertable,
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