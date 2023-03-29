from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('paynow/<fees>/<patid>/<docid>/<meetid>/', views.paynow, name = 'paynow'),
    path('sslc/status/', views.sslc_status, name = 'sslc_status'),
    path('payforsub/', views.payforsub, name='payforsub'),    
    path('substatus/', views.substatus, name = 'substatus'),
]
    