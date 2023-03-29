from django.shortcuts import render
from . import forms
from meeting.models import *
import requests
from django.conf import settings
from django.shortcuts import render
import base64
from zoomus import ZoomClient
import urllib.parse
import requests
import datetime
from response.models import *
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
import requests
from oauthlib.oauth2 import WebApplicationClient
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime, timezone
import requests
from django.conf import settings
from pytz import timezone as pytz_timezone
from django.utils import timezone
from request.models import *

def authorize(request):
    print ('checking testind debugging')
    # Create an instance of the WebApplicationClient class
    client = WebApplicationClient(settings.ZOOM_CLIENT_ID)

    # Construct the authorization URL
    redirect_uri = request.build_absolute_uri(reverse('zoom_callback'))
    authorization_url = client.prepare_request_uri(
        'https://zoom.us/oauth/authorize', redirect_uri=redirect_uri)
    print (authorization_url)
    # Redirect the user to the authorization URL
    return redirect(authorization_url)

def zoom_callback(request):
    # Create an instance of the WebApplicationClient class
    client = WebApplicationClient(settings.ZOOM_CLIENT_ID)

    # Exchange the authorization code for an access token
    redirect_uri = request.build_absolute_uri(reverse('zoom_callback'))
    token_url = 'https://zoom.us/oauth/token'
    authorization_response = request.build_absolute_uri()
    response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': request.GET.get('code'),
        'redirect_uri': redirect_uri,
    }, auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET))

    # Store the access token in the session
    request.session['zoom_access_token'] = response.json()['access_token']
    print(request.session['zoom_access_token'], "access token")
    # Redirect the user to the meeting page
    return redirect('doctor_pending')


def create_zoom_meeting(request, topic, start_datetime, duration, password):
    # Get the access token from the session
    access_token = request.session['zoom_access_token']

    # Set up the headers for the API request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # Set up the data for the API request
    data = {
        'topic': topic,
        'type': 2,
        'start_time': start_datetime.astimezone(pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'duration': duration,
        'agenda': 'Testing Zoom API',
        'settings': {
            'host_video': 'true',
            'participant_video': 'true',
            'join_before_host': 'true',
            'mute_upon_entry': 'false',
            'waiting_room': 'true',
            'auto_recording': 'cloud',
            'enforce_login': 'false',
            'enforce_login_domains': '',
            'approval_type': 2,
            'registration_type': 1,
            'audio': 'voip',
            'auto_start_recording': 'true'
        }
    }
    
    # Send a POST request to the Zoom API to create a meeting
    response = requests.post(
        'https://api.zoom.us/v2/users/me/meetings',
        headers=headers,
        json=data
    )

    # Return the response from the API
    return response.json()

    
    # Send a POST request to the Zoom API to create a meeting
    response = requests.post(
        'https://api.zoom.us/v2/users/me/meetings',
        headers=headers,
        json=data
    )

    # Return the response from the API
    return response.json()

import pytz
from pytz import timezone

def create_meeting(request, userid, patientid, emgreqid):
    # Get the necessary parameters from the request
    
    if not request.user.is_authenticated:
        return redirect ('signin')
    context = {}
    userid = int(userid)
    patientid = int(patientid)
    emgreqid = int(emgreqid)
    context['emgreqid'] = emgreqid
    context['patientid'] = patientid
    context['userid'] = userid
    if request.method == "POST":
        topic = request.POST.get('topic')
        start_time_str = request.POST.get('startdatetime')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        tz = pytz.timezone(settings.TIME_ZONE)
        start_time = tz.localize(start_time)
        start_time_utc = start_time.astimezone(pytz.utc)
        duration = request.POST.get('duration')
        password = request.POST.get('password')
        response = create_zoom_meeting(request, topic, start_time_utc, duration, password)
        print(response)
        #Redirect the user to the Zoom join URL
        print(response['join_url'])
        #user_profile = 
        
        print (userid, patientid)
        doctor_profile = UserProfile.objects.get(user = request.user)
        print(doctor_profile)
        creator_profile = UserProfile.objects.get(id = userid)
        print (creator_profile)
        patient_profile = Patient.objects.get(id = patientid)
        print(patient_profile)
        responseobj = Response.objects.create(doctor_profile = doctor_profile, user_profile = creator_profile, patient_profile = patient_profile)
        responseobj.doctorack = "Accepted"
        responseobj.join_url = response['join_url']
        responseobj.start_meeting_url = response['start_url']
        responseobj.scheduled_datetime = start_time
        responseobj.instructions = request.POST.get('instructions')
        responseobj.meeting_duration = request.POST.get('duration')
        responseobj.topic = request.POST.get('topic')
        responseobj.save()
        emgreqobj = Emgergency.objects.get(id = emgreqid)
        emgreqobj.status = "Accepted"
        emgreqobj.save()
        return redirect('scheduled_meeting')
    return render(request, 'meeting/create_meeting.html', context)


def conf(request):
    return render(request, 'meeting/conf.html')

def searchmeeting(request):
    return render(request, 'user/home.html', context = dict)

''' Meeting page a prothome sob meeting thakbe active user er. Then app a joto meeting hoice seigula thakbe. '''
def meetinglist(request):
    return render(request, 'user/home.html', context = dict)

def meetingdetails(request, meetingid):
    return render(request, 'user/home.html', context = dict)
