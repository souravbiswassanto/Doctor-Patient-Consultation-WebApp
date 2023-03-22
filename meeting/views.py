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

def authorize(request):
    # Create an instance of the WebApplicationClient class
    client = WebApplicationClient(settings.ZOOM_CLIENT_ID)

    # Construct the authorization URL
    redirect_uri = request.build_absolute_uri(reverse('zoom_callback'))
    authorization_url = client.prepare_request_uri(
        'https://zoom.us/oauth/authorize', redirect_uri=redirect_uri)

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
    return redirect('create_meeting')


def create_zoom_meeting(request,topic, start_time, duration, timezone, password):
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
    'start_time': start_time,
    'duration': duration,
    'timezone': timezone,
    'agenda': 'Testing Zoom API',
    'settings': {
        'host_video': 'true',
        'participant_video': 'true',
        'join_before_host': 'true',
        'mute_upon_entry': 'false',
        'auto_recording': 'cloud'
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



def create_meeting(request):
    # Get the necessary parameters from the request
    if request.method == "POST":
        topic = request.POST.get('topic')
        start_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        duration = request.POST.get('duration')
        tz = settings.TIME_ZONE  # Replace with your own timezone
        password = request.POST.get('password')
        num_meetings = 2

        # Create the Zoom meetings
        for i in range(num_meetings):
            response = create_zoom_meeting(request, f"{topic} {i}", start_time, duration, tz, password)
            print(response)
            print(response['join_url'])
        # Create the Zoom meeting
        #response = create_zoom_meeting(request,topic, start_time, duration, tz, password)
        #print (response)
        # Redirect the user to the Zoom join URL
        #print(response['join_url'])
        return redirect(response['join_url'])
    return render(request, 'meeting/create_meeting.html')


def consultation(request):
    if request.method == 'POST':
        # Get access token using client id and client secret
        token_url = "https://zoom.us/oauth/token?grant_type=client_credentials"
        client_id = settings.ZOOM_CLIENT_ID
        client_secret = settings.ZOOM_CLIENT_SECRET
        headers = {'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}
        response = requests.post(token_url, headers=headers)
        access_token = response.json()['access_token']

        # Create a Zoom meeting
        meeting_url = f"https://api.zoom.us/v2/users/{settings.ZOOM_USER_ID}/meetings"
        headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
        data = {
            "topic": "Consultation Meeting",
            "type": 2,
            "duration": 30,
            "timezone": "Asia/Dhaka",
            "settings": {
                "host_video": "true",
                "participant_video": "true",
                "join_before_host": "true",
                "mute_upon_entry": "true",
                "watermark": "true",
                "approval_type": 2
            }
        }
        response = requests.post(meeting_url, headers=headers, json=data)
        print (response.status_code)
        if response.status_code == 201:
            meeting_data = response.json()
            meeting_id = meeting_data['id']
            join_url = meeting_data['join_url']
            # Send meeting details to user
            # You can use your preferred method of communication to send the meeting details to the user
            # For example, you can send an email to the user with the meeting details.
            return render(request, 'meeting/consultation.html', {'message': f'Meeting created with meeting ID: {meeting_id} and join URL: {join_url}'})
        else:
            print(response.json())  # Print the error message to the console
            return render(request, 'meeting/consultation.html', {'error': 'Failed to create meeting'})
    else:
        # Render the consultation page with user details
        return render(request, 'meeting/consultation.html')

def conf(request):
    return render(request, 'meeting/conf.html')

def searchmeeting(request):
    return render(request, 'user/home.html', context = dict)

''' Meeting page a prothome sob meeting thakbe active user er. Then app a joto meeting hoice seigula thakbe. '''
def meetinglist(request):
    return render(request, 'user/home.html', context = dict)

def meetingdetails(request, meetingid):
    return render(request, 'user/home.html', context = dict)
