from django.shortcuts import render
from . import forms
from meeting.models import *

def searchmeeting(request):
    return render(request, 'user/home.html', context = dict)

''' Meeting page a prothome sob meeting thakbe active user er. Then app a joto meeting hoice seigula thakbe. '''
def meetinglist(request):
    return render(request, 'user/home.html', context = dict)

def meetingdetails(request, meetingid):
    return render(request, 'user/home.html', context = dict)
