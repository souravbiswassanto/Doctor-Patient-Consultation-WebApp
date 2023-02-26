from django.shortcuts import render
from . import forms
from request.models import *

def Response(request):
    return render(request, 'user/home.html', context = dict)

def Responseaction(request):
    return render(request, 'user/home.html', context = dict)
