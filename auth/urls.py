from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('verify_otp/', views.verify_otp, name = "verify_otp"),
    path('resend_otp/', views.resend_otp, name = 'resend_otp'),
    path('signin/', views.signin, name = 'signin'),
    path('logout/',views.logout_view, name = 'logout'),
    path('userprofile/', views.userprofile, name = 'userprofile'),
    path('rating/<id>/', views.rating, name = 'rating'),
]
