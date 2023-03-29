from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('Response/', views.Response, name = 'Response'),
    path('Responseaction/', views.Responseaction, name = 'Responseaction'),
    path('scheduled_meeting/', views.scheduled_meeting, name = 'scheduled_meeting'),
    path('room/', views.room, name = 'room'),
    path('openroom/', views.openroom, name = 'openroom'),
    path('dltfile/<int:file_id>/<int:ptid>/<int:mtid>/', views.dltfile, name = 'dltfile'),
]
