from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('Request/', views.Request, name = 'Request'),
    path('generalrequest/', views.generalrequest, name = 'generalrequest'),
    path('emgrequest/', views.emgrequest, name = 'emgrequest'),
    path('laterequest/', views.laterequest, name = 'laterequest'),
    path('generalrequestaction/', views.generalrequestaction, name = 'generalrequestaction'),
    path('emgrequestaction/', views.emgrequestaction, name = 'emgrequestaction'),
    path('laterequestaction/', views.laterequestaction, name = 'laterequestaction'),
    
]
