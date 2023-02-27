import phonenumbers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django_otp import devices_for_user
import phonenumbers
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.shortcuts import render, redirect
from django.contrib import messages
from django_otp import user_has_device

from user.models import Userdata
from user.models import UserProfile


# def signup(request):
#     if request.method == 'POST':
        
#         phone_number = request.POST.get('phone_number')
#         role = request.POST.get('role')
#         password = request.POST.get('password')
#         password_confirm = request.POST.get('password_confirm')
        
#         # Perform validation
#         if password != password_confirm:
#             messages.error(request, 'Passwords do not match.')
#             return redirect('signup')
        
#         # Validate phone number
#         try:
#             parsed_phone_number = phonenumbers.parse(phone_number, None)
#             if not phonenumbers.is_valid_number(parsed_phone_number):
#                 raise ValueError('Invalid phone number.')
#         except phonenumbers.phonenumberutil.NumberParseException:
#             messages.error(request, 'Invalid phone number.')
#             return redirect('signup')
        
#         # Check if user with this phone number already exists
#         if UserProfile.objects.filter(phone_number=phone_number).exists():
#             messages.error(request, 'A user with this phone number already exists.')
#             return redirect('signup')
        
#         # Generate OTP
#         otp = random.randint(100000, 999999)
        
#         # Save the OTP to the session
#         request.session['signup_otp'] = str(otp)
#         request.session['signup_phone_number'] = phone_number
#         request.session['signup_role'] = role
#         request.session['signup_password'] = password
        
#         # Send the OTP to the user via SMS or email using django_otp
#         user = UserProfile.objects.create_user(phone_number = phone_number, password=password)
#         device = TOTPDevice.objects.create(user=user, name='default')
#         device.generate_secret()
#         device.save()
#         device_config = device.config.copy()
#         device_config.update({
#             'name': device.name,
#             'step': device.step,
#             'digits': device.digits,
#         })
#         otp = device.generate_challenge()
#         device.save()
#         messages.success(request, 'OTP sent to your phone number.')
        
#         # Redirect to the OTP verification page
#         return redirect('verify_otp')
    
#     return render(request, 'signin/signup.html')

# def verify_otp(request):
#     if 'signup_otp' not in request.session:
#         messages.error(request, 'Invalid request.')
#         return redirect('signup')
    
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         saved_otp = request.session['signup_otp']
        
#         if otp == saved_otp:
#             # Save the user to the database
#             phone_number = request.session['signup_phone_number']
#             role = request.session['signup_role']
#             password = request.session['signup_password']
            
#             # Create a new user
#             user = Userdata.objects.create_user(
#                 username=phone_number,
#                 password=password,
#                 role=role
#             )
            
#             # Check if the user has a registered OTP device
#             if user_has_device(user):
#                 # Generate a new OTP
#                 otp = user.authenticator.generate_challenge()
                
#                 # Save the OTP to the session
#                 request.session['login_otp'] = str(otp)
#                 request.session['login_phone_number'] = phone_number
                
#                 # Send the OTP to the user via SMS or email
#                 # Code for sending OTP via SMS or email goes here
                
#                 # Redirect to the OTP verification page for login
#                 return redirect('login_otp')
            
#             # Clear the session variables
#             del request.session['signup_otp']
#             del request.session['signup_phone_number']
#             del request.session['signup_role']
#             del request.session['signup_password']
            
#             messages.success(request, 'Your account has been created. Please log in.')
#             return redirect('login')
        
#         messages.error(request, 'Invalid OTP.')
    
#     return render(request, 'signin\verify_otp.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
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
            if not phonenumbers.is_valid_number(parsed_phone_number):
                raise ValueError('Invalid phone number.')
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
        
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
                                     .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                                     .verification_checks \
                                     .create(to=f"{phone_number}", code=otp)
        if verification_check.status == 'approved':
            user = authenticate(request, phone_number=phone_number)
            login(request, user)
            return redirect('userhome')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('verify_otp')
    else:
        return render(request, 'signin/verify_otp.html')
