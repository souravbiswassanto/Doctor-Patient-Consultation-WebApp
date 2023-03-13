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
    path('showpatients/', views.showpatients, name = 'showpatients'),

] 

