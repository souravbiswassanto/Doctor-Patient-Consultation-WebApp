from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('meetinglist/', views.meetinglist, name = 'meetinglist'),
    path('meetingdetails/', views.meetingdetails, name = 'meetingdetails'),
    path('searchmeeting/', views.searchmeeting, name = 'searchmeeting'),
    
]
