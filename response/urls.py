from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('Response/', views.Response, name = 'Response'),
    path('Responseaction', views.Responseaction, name = 'Responseaction'),
]
