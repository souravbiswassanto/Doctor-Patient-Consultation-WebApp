from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('form/', views.form, name = 'doctorform'),
    path('home/', views.home, name = 'doctorhome'),
    
]
