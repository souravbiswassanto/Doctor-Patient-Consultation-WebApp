from django.shortcuts import render
from . import forms
from request.models import *

def Request(request):
    return render(request, 'user/home.html', context = dict)


def generalrequest(request):
    return render(request, 'user/home.html', context = dict)

def emgrequest(request):
    return render(request, 'user/home.html', context = dict)

def laterequest(request):
    return render(request, 'user/home.html', context = dict)

def generalrequestaction(request):
    return render(request, 'user/home.html', context = dict)

def emgrequestaction(request):
    return render(request, 'user/home.html', context = dict)

def laterequestaction(request):
    return render(request, 'user/home.html', context = dict)
