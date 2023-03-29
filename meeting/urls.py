from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.models import UserProfile
from . import views
urlpatterns = [
    path('meetinglist/', views.meetinglist, name = 'meetinglist'),
    path('meetingdetails/', views.meetingdetails, name = 'meetingdetails'),
    path('searchmeeting/', views.searchmeeting, name = 'searchmeeting'),
    path('create_meeting/<int:userid>/<int:patientid>/<int:emgreqid>/', views.create_meeting, name = 'create_meeting'),
    path('conf/', views.conf, name = 'conf'),
    path('zoom/authorize/', views.authorize, name='zoom_authorize'),
    path('zoom/callback/', views.zoom_callback, name='zoom_callback'),
    
]
