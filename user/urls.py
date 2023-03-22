from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [ 
    path('home/', views.userhome, name = 'userhome'),
    path('form/', views.form, name = 'userform'),
    path('createpatient/', views.createpatient, name = 'createpatient'),
    path('profile/', views.profile, name = 'profile'),
    path('showpatients/', views.showpatients, name = 'showpatients'),
    path('doctor_detail/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('findin/', views.findin, name = 'findin'),
    path('delete_patient/<int:pt_id>/', views.delete_patient, name = 'delete_patient'),
    path('patient_accepted/', views.patient_accepted, name = 'patient_accepted'),
    path('patient_pending/', views.patient_pending, name = 'patient_pending'),
    path('patient_declined/', views.patient_declined, name = 'patient_declined'),

] 

