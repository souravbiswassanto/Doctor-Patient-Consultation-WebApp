from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('form/', views.form, name = 'doctorform'),
    path('home/', views.home, name = 'doctorhome'),
    path('profile/', views.profile, name = 'profile'),
    path('meetinglist/', views.meetinglist, name = 'meetinglist'),
    path('meetingdetails/', views.meetingdetails, name = 'meetingdetails'),
    path('doctor_pending/', views.doctor_pending, name = 'doctor_pending'),
    path('doctor_accepted/', views.doctor_accepted, name = 'doctor_accepted'),
    path('doctor_declined/', views.doctor_declined, name = 'doctor_declined'),
    path('decline_patient/<int:dec_id>', views.decline_patient, name = 'decline_patient',)
]
