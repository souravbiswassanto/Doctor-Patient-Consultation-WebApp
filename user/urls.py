from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('home/', views.home, name = 'userhome'),
    path('form/', views.form, name = 'userform'),
] 

