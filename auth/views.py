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
from django.utils import timezone
from user.models import Userdata
from user.models import UserProfile
from django.contrib.auth import logout
from django.conf import settings
from twilio.rest import Client
from django.core.exceptions import ObjectDoesNotExist
from twilio.base.exceptions import TwilioRestException
from django.contrib.auth.hashers import check_password
from doctor.models import *
from user import forms as uf
from doctor import forms
from django.contrib.auth import update_session_auth_hash

def signup(request):
    if request.method == 'POST':
        # Get form values
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']
        
        
        try:
            user = User.objects.get(username=phone_number)
        except User.DoesNotExist:
            user = None
        
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None
        
        if user and not user_profile.otp_verified:
            request.session['phone_number'] = phone_number
            request.session['password'] = password1
            messages.error(request, 'Phone number already exist and you need to verify otp')
            return redirect('verify_otp')
        
        # Validate phone number
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            messages.error(request, 'Phone number already exists')
            request.session['phone_number'] = phone_number
            return redirect('signup')
        except ObjectDoesNotExist:
            pass
            
        try:
            parsed_phone_number = phonenumbers.parse(phone_number, "BD") # Use the country code
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
        request.session['phone_number'] = phone_number
        user_profile = UserProfile.objects.create(user=user, phone_number=phone_number, role=role)
        user_profile.save()
        
        #Send OTP
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            verification = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone_number, channel='sms')
            request.session['phone_number'] = phone_number
            request.session['password'] = password1
            
        except TwilioRestException as e:
            messages.error(request, f'Error: {e.msg}')
            return redirect('signup')
        
        return redirect('verify_otp')
    else:
        return render(request, 'signin/signup.html')


def verify_otp(request):
    if request.method == 'POST':
        phone_number = request.session.get('phone_number')
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
            user = authenticate(request, username=User.objects.get(username = phone_number))
            password = request.session.get('password', None)
            user = authenticate(request, username=User.objects.get(username = phone_number), password=password)
            login(request, user)
            request.session['phone_number'] = phone_number
            user_profile.otp_verified = True
            user_profile.save()
            user_profile.join_date = timezone.now()
            user_profile.last_seen = timezone.now()
            userdata = Userdata.objects.create(user_profile = user_profile)
            userdata.image = str(settings.DEFAULT_IMAGE)
            userdata.save()
            return redirect('userhome')
        else:
            messages.error(request, 'Invalid OTP')
            request.session['phone_number'] = phone_number
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
        print(e.msg)
        messages.error(request, f'Error: {e.msg}')
    return redirect('verify_otp')



def signin(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=phone_number)
        except User.DoesNotExist:
            user = None
        
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None
        
        if user and not user_profile.otp_verified:
            request.session['phone_number'] = phone_number
            messages.error(request, 'Phone number already exist and you need to verify otp')
            return redirect('verify_otp')
        
        try:
            user = authenticate(request, username=User.objects.get(username = phone_number), password=password)
            
            if user is not None:
                request.session['phone_number'] = phone_number
                login(request, user)
                request.session['phone_number'] = phone_number
                print(request.session)
                print (request.session['phone_number'], ' hellow rosld ')
                user_profile.last_seen = timezone.now()
                return redirect('userhome')
            else:
                messages.error(request, 'Invalid phone number or password')
                
                return redirect('signin')
        except Exception as e:
            messages.error(request, 'Error: ' + str(e))
            return redirect('signin')
        
    return render(request, 'signin/signin.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def userprofile(request):
    
    phone_number = request.session.get('phone_number')
    #print (phone_number)
    user_profile = UserProfile.objects.get(phone_number = phone_number)
    user_profile.last_seen = timezone.now()
    context = {}
    form = None
    patientlist = Patient.objects.filter(user_profile=user_profile).order_by('-created_at')
    context['patientlist'] = patientlist
    
    context['user_profile'] = user_profile
    role = user_profile.role
    #print(user_profile,'souravvvvvvvvvvvvvvvvv')
    #print(type(user_profile))
    if role == 'user' or role == 'User':
        form = uf.Userform()
    if role == 'doctor' or role == 'Doctor':
        form = forms.Doctorform()
    #form['user_profile']= user_profile
    context['form'] = form
    data = None
    if role == 'user' or role == 'User':
        data = Userdata.objects.get(user_profile = user_profile)
    if role == 'doctor' or role == 'Doctor':
        data = Doctordata.objects.get(user_profile = user_profile)
    #print (user_profile)
    #print (role)
    #print('user profile printed')
    context['data'] = data
    doctor = Doctordata.objects.all()
    context['doctor'] = doctor
    
    if request.method == 'POST':
        up = None
        userdata = None
        if role == 'user' or role == 'User':
            up = Userdata.objects.get(user_profile = user_profile)
            userdata = uf.Userform(request.POST, request.FILES, instance=up)
        if role == 'doctor' or role == 'Doctor':
            up = Doctordata.objects.get(user_profile = user_profile)
            userdata = forms.Doctorform(request.POST, request.FILES, instance=up)
     
        userdata.user_profile = user_profile
        if userdata.is_valid():
            #print (userdata.cleaned_data['name'])
            old_password = userdata.cleaned_data['oldpassword']
            new_password = userdata.cleaned_data['newpassword']
            confirm_password = userdata.cleaned_data['confirmpassword']
            
            if old_password == None:
                userdata.save(commit=True)
                return redirect('userprofile')
            
            if not request.user.check_password(old_password):
                messages.error(request, 'Your old password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                userdata.save(commit=True)
                messages.success(request, 'Your password has been updated.')
                return redirect('userprofile')
        return redirect('userprofile')
    
    if role == 'user' or role == 'User':
        return render(request, 'signin/userprofile.html', context)
    else:
        return render(request, 'signin/doctorprofile.html', context)
