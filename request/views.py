from django.shortcuts import render
from . import forms
from request.models import *
from django.shortcuts import render
from . import forms
from request.models import *
from django.shortcuts import render
from . import forms
from doctor.models import *
from response.models import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . import forms
import pytz
from user.models import *
from doctor.models import *
import random
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.models import UserProfile
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.contrib import messages
from meeting import forms as meeting_form
from user import forms as user_form
from doctor import forms as doctor_form
from doctor.models import *
from meeting.models import *
from auth.models import *
from request.models import *
from meeting.models import *

from request import forms as request_form
from datetime import datetime
import json

import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

def paynow(request, fees, patid, docid, meetid):
    fees = int(fees)
    if not request.user.is_authenticated:
        return redirect('signin')
    user_profile = UserProfile.objects.get(user = request.user)
    if user_profile is not None:
        user_profile.last_seen = timezone.now()
        user_profile.save()
    if user_profile.role == "Doctor" or user_profile.role == "doctor":
        return redirect('scheduled_meeting')
    
    userid = request.user.id
    store_id = settings.SSLCOMMERZ_STORE_ID
    store_pass = settings.SSLCOMMERZ_STORE_PASSWD
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id= store_id, sslc_store_pass= store_pass)
    status_url = request.build_absolute_uri(reverse('sslc_status'))
    
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    mypayment.set_product_integration(total_amount=Decimal(fees), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=1, shipping_method='YES', product_profile='None')
    mypayment.set_customer_info(name='John Doe', email='johndoe@gmail.com', address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01881178367')
    mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')
    mypayment.set_additional_values(value_a= userid, value_b= patid, value_c= docid, value_d= meetid)
    response_data = mypayment.init_payment()

    print(response_data)
    print (response_data['GatewayPageURL'])
    
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def sslc_status(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        user = User.objects.get(id = int(payment_data['value_a']))
        #doctor = UserProfile.objects.get(id = int(payment_data['value_b']))
        #patient = Patient.objects.get(id = int(payment_data['value_c']))
        #meeting = Response.objects.get(id = int(payment_data['value_d']))
        request.user = user
        status = payment_data['status']
        print(status)
        login(request, user)
        user_profile = UserProfile.objects.get(user = request.user)
        context = {}
        context['user_profile'] = user_profile
        role = user_profile.role
        data = None
        
        data = Response.objects.filter(user_profile = user_profile)
        #data = Response.objects.filter()
        datas = []
        context['role'] = role
        if status == "VALID":
            messages.success(request, "Your Payement was succesfull, wait for the host to start meeting")
        if status == "FAILED":
            messages.error(request, "Unsuccessfull Payment, try agian.")
        for ds in data:
            dd = ds.patient_profile
            dd.created_at = ds.scheduled_datetime
            
            if ds.id == int(payment_data['value_d']):
                ds.payment_status = status
                ds.save()
            de = Doctordata.objects.get(user_profile=ds.doctor_profile)
            
                
            lst = (dd, de, ds, ds.id)
            print (lst)
            datas.append(lst)
        
        context['resultset'] = datas 
        return render(request, 'response/responses.html', context)
    

def payforsub(request):
    fees = int(1000)
    if not request.user.is_authenticated:
        return redirect('signin')
    user_profile = UserProfile.objects.get(user = request.user)
    if user_profile is not None:
        user_profile.last_seen = timezone.now()
        user_profile.save()
    if user_profile.is_sub:
        messages.success(request, 'you are already a subscriber')
        return redirect('userhome')
    
    
    
    userid = request.user.id
    store_id = settings.SSLCOMMERZ_STORE_ID
    store_pass = settings.SSLCOMMERZ_STORE_PASSWD
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id= store_id, sslc_store_pass= store_pass)
    status_url = request.build_absolute_uri(reverse('substatus'))
    
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
    mypayment.set_product_integration(total_amount=Decimal(fees), currency='BDT', product_category='clothing', product_name='demo-product', num_of_item=1, shipping_method='YES', product_profile='None')
    mypayment.set_customer_info(name='John Doe', email='johndoe@gmail.com', address1='demo address', address2='demo address 2', city='Dhaka', postcode='1207', country='Bangladesh', phone='01881178367')
    mypayment.set_shipping_info(shipping_to='demo customer', address='demo address', city='Dhaka', postcode='1209', country='Bangladesh')
    mypayment.set_additional_values(value_a= userid, value_b= '', value_c= '', value_d= '')
    response_data = mypayment.init_payment()

    print(response_data)
    print (response_data['GatewayPageURL'])
    
    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def substatus(request):
    if request.method == 'POST' or request.method == 'post':
        payment_data = request.POST
        user = User.objects.get(id = int(payment_data['value_a']))
        request.user = user
        status = payment_data['status']
        login(request, user)
        user_profile = UserProfile.objects.get(user = request.user)
        if status == "VALID":
            messages.success(request, "Your Payement was succesfull, You are now a subscriber")
            user_profile.is_sub = True
            user_profile.save()
            return redirect('userhome')
        else:
            messages.error(request, "Your Payement was unsuccesfull")
            return redirect('userhome')
        