import phonenumbers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django_otp import devices_for_user
import random
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import user_has_device

from user.models import Userdata
from user.models import UserProfile

from django.conf import settings
from twilio.rest import Client
from django.core.exceptions import ObjectDoesNotExist
from twilio.base.exceptions import TwilioRestException


def signup(request):
    if request.method == 'POST':
        # Get form values
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']
        
        # Validate phone number
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            messages.error(request, 'Phone number already exists')
            return redirect('signup')
        except ObjectDoesNotExist:
            pass
            
        try:
            parsed_phone_number = phonenumbers.parse(phone_number, "IN") # Use the country code
            print (phonenumbers.is_valid_number(parsed_phone_number))
            if not phonenumbers.is_valid_number(parsed_phone_number):
                #raise ValueError('Invalid phone number.')
                messages.error(request, 'Invalid phone number.')
                return redirect('signup')
            
            phone_number = phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)
            
        except phonenumbers.phonenumberutil.NumberParseException:
            messages.error(request, 'Invalid phone number.')
            return redirect('signup')
        
        # Validate passwords
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=phone_number)
        user.set_password(password1)
        user.save()
        
        user_profile = UserProfile.objects.create(user=user, phone_number=phone_number, role=role)
        user_profile.save()
        
        # Send OTP
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            verification = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone_number, channel='sms')
            request.session['phone_number'] = phone_number
        except TwilioRestException as e:
            messages.error(request, f'Error: {e.msg}')
            return redirect('signup')
        
        return redirect('verify_otp')
    else:
        return render(request, 'signin/signup.html')


def verify_otp(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')
        print(phone_number)
        otp = request.POST.get('otp')
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
        except ObjectDoesNotExist:
            user_profile = None
            
        if not user_profile:
            messages.error(request, 'Invalid phone number')
            return redirect('signup')
        try:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            verification_check = client.verify \
                                        .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                                        .verification_checks \
                                        .create(to=f"{phone_number}", code=otp)
        except TwilioRestException as e:
            #messages.error(request, f'Error: {e.msg}')
            messages.error(request, 'Otp verification failed. Try again!')
            return redirect('verify_otp')
        
        if verification_check.status == 'approved':
            user = authenticate(request, phone_number=phone_number)
            login(request, user)
            return redirect('userhome')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('verify_otp')
    else:
        return render(request, 'signin/verify_otp.html')



def resend_otp(request):
    phone_number = request.session.get('phone_number')
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        verification = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone_number, channel='sms')
        messages.success(request, 'OTP sent successfully.')
    except TwilioRestException as e:
        messages.error(request, f'Error: {e.msg}')
    return redirect('verify_otp')
