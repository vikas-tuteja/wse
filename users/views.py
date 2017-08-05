# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django_redis import get_redis_connection
from django.contrib.auth import login as auth_login

from models import UserDetail, UserRole, CandidateAttribute
from utility.utils import ComputeCompletion
from serializers import UserSerializer, AuthUserSerializer, UserMeterSerializer
from events.views import EventListing
from events.models import AllocationStatus
from events.serializers import ProfileEventSerializer
from utility import mygenerics

from filters import UserFilters

# Create your views here.

class CreateUser( generics.CreateAPIView ):
    """
    To create a new user, we require only 3 mandatory fields
    user name which will be the same as email
    password and 10 digit mobile 
    METHOD : POST
    POST PARAMS: email
               : password
               : user_role
               : mobile
    
    PS: if not password, then mobile = password
    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()

    def post(self, request, *args, **kwargs):
        status = False
        kwargs.update(request.POST.dict())
        
        # check if user already exists
        email = kwargs.get('username', kwargs.get('email'))
        mobile = kwargs.get('mobile')[-10:]
        exists = UserDetail.objects.filter(
            Q(auth_user__username=email) | Q(auth_user__email=email) | Q(mobile=mobile) 
        )

        if not exists:
            try:
                # create auth user first
                auth_user = User.objects.create(
                    username = email,
                    email = email,
                )
                auth_user.set_password(kwargs.get('password', kwargs.get('mobile')))
                auth_user.save()
                
                # then create userdetails
                user_detail = UserDetail.objects.create(
                    auth_user = auth_user,
                    type = UserRole.objects.get(slug=kwargs.get('user_role', 'candidate')),
                    mobile = mobile,
                )
                user_detail.save()
            
                # automatic login after registration
                user = authenticate( username = kwargs.get('username', kwargs.get('email')), password = kwargs.get('password') )
                auth_login(request, user)

                status = True
                message = 'User created successfully'

            except IntegrityError:
                message = 'User with this email or mobile already exists '
        else:
            message = 'User with this email or mobile already exists '

        return JsonResponse(data={
            'status':status,
            'message':message
        })
        
class Logout():
    pass
    #TODO remove user from session as well as request 

class LoginUser( generics.ListAPIView ):
    """
    METHOD : GET
    POST PARAMS: email
               : password
    """
    serializer_class = AuthUserSerializer
    queryset = User.objects.none()
    
    def get(self, request, *args, **kwargs):
        kwargs.update(request.GET.dict())
        status = False
        user = authenticate( username = kwargs.get('username', kwargs.get('email')), password = kwargs.get('password') )

        if not user:
            message = 'Error: Invalid credentials'
        else:
            auth_login(request, user)
            status = True
            message = 'Successfully logged in'

        return JsonResponse( data={
            'status':status,
            'message':message,
        })


class ForgotPassword( generics.UpdateAPIView ):
    """
    this will change the password of the user to 
    his/her 10 digit mobile number
    METHOD : PUT
    POST PARAMS: email

    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()

    def put(self, request, *args, **kwargs):
        status = False
        email = request.POST.get('username')
        if not email:
            message = 'Error: Please enter username.'

        else:
            userObj = UserDetail.objects.get(auth_user__email=email)
            if not userObj:
                message = 'Error: %s user not found.' % email
            else:
                userObj.auth_user.set_password( str(userObj.mobile)[-10:] )
                userObj.auth_user.save()
                status = True
                message = 'Your new password is your 10 digit mobile number.'

        return JsonResponse(data={
            'status':status,
            'message':message
        })



class ChangePassword( generics.UpdateAPIView ):
    """
    changing the password to a new password
    METHOD : PUT
    POST PARAMS: email
               : password
               : new password
    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.none()
    lookup_field = "auth_user__email"
    lookup_url_kwarg = "user_email"

    def put(self, request, *args, **kwargs):
        status = False
        kwargs.update(request.POST.dict())
        auth_user = authenticate( 
            username = kwargs.get('email'),
            password = kwargs.get('password')
        )
        auth_login(request, auth_user)

        if not getattr(request.user, 'email', None):
            message = 'Error: Old Password is incorrect'

        else:
            auth_user.set_password(kwargs.get('new_password'))
            auth_user.save()
            status, message = True, 'Password changed Successfully'

        return JsonResponse(data={
            'status':status,
            'message':message
        })


class CheckUsernameExists( generics.ListAPIView ):
    """
    check in redis "key : usernames" if the user already exists with us
    return True if the username already exists, else False
    GET params : username
    
    """
    serializer_class = AuthUserSerializer
    queryset = UserDetail.objects.none()

    def get(self, request, *args, **kwargs ):

        status, message = False, str()
        username = request.GET.get('username')
        if not username:
            message = 'Invalid params: Please pass username'

        else:
            con = get_redis_connection('default')
            status = con.sismember("usernames", username)
            

        return JsonResponse(data={
            'status':status,
            'message':message
        })


class UserProfileCompletionMeter( generics.ListAPIView ):
    """
    calculates the percentage of user profile completion
    input params: username
    output: a number that indicates the percentage of user profile competed
    logic : (no of column filled / total no of column ) * 100

    """
    serializer_class = UserMeterSerializer
    queryset = UserDetail.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilters

    def get(self, *args, **kwargs):
        response = super(UserProfileCompletionMeter, self).get(*args, **kwargs)
        try:
            candidate_info = response.data['results'][0]['candidate']
            del response.data['results'][0]['candidate']
            response.data['results'][0].update(candidate_info)
        except:
            pass

        # TODO get CANDIDATEATTRIBUTE all fileds + USERDETAIL ALL FIELDS
        # assuming that one record will be found in response.data
        meter = ComputeCompletion(response.data['results'])
        
        return JsonResponse(data={
            'profile_completed':meter.compute_percent(),
        })

class UpdateUserInfo( generics.UpdateAPIView ):
    """
    update user profile basic information in UserDetail Table
    can update 3 table Auth_user, UserDetail or CandidateAttribute, not applicaable for clients, co-ordinators

    """
    serializer_class = UserMeterSerializer
    queryset = UserDetail.objects.none()
    user_dict = {
        'user': ('first_name', 'last_name'),
        'userdetail': ('mobile', 'whatsapp_number', 'address', 'image', 'area', 'city', 'state'),
        'candidateattribute': ('language_proficiency', 'looks', 'open_to_which_kind_of_job', 'pay_scale', 'comfortable_travelling_outdoor', 'comfortable_for_liquor_promotion', 'comfortable_working_at_odd_timings', 'candidate_profile')
    }

    def put(self, request, *args, **kwargs):
        """ 
            TABLE auth_user : first_name, last_name
            TABLE USERDETAIL : mobile, whatsapp_number, address, image, area, city, state
            TABLE CandidateAttribute : language_proficiency, looks, open_to_which_kind_of_job, pay_scale, comfortable_travelling_outdoor, comfortable_for_liquor_promotion, comfortable_working_at_odd_timings, candidate_profile
            """
        user, userdetail, candidateattribute = {}, {}, {}
        # TODO change this to POST after integration
        kwargs.update(request.GET.dict())
        for model, keys in self.user_dict.items():
            for key in keys:
                if key in kwargs and kwargs[key] not in (None, ''):
                    eval("%s.update({ key:kwargs[key] })" % model)

        # TODO test this
        # update auth_user attributes
        User.objects.filter(id=request.user.id).update(**user)

        # update userdetails
        ud = UserDetail.objects.filter(auth_user=request.user)
        ud.update(**userdetail)

        # check if candidateattribute exists or not, create/update its attributes accordingly
        ca = CandidateAttribute.objects.filter(user=ud[0])
        if ca:
            ca.update(**candidateattribute)
        else:
            ca = CandidateAttribute.objects.create(**candidateattribute)
            ca.save()

        return JsonResponse(data={
            'status': True,
            'message': 'Profile Info Updated Successfully'
        })


class UserProfile( generics.ListAPIView, mygenerics.RelatedView ):
    """
    /my-profile/ page 
    get users event info

    """
    serializer_class = UserSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = UserFilters
    template_name = 'users/my_profile_base.html'

    def get_queryset(self, *args, **kwargs):
        if self.request._request.user:
            queryset = UserDetail.objects.filter(auth_user=self.request._request.user)
        else:
            queryset = UserDetail.objects.filter()
        return queryset

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse(data={
                'status': False,
                'message': 'Unauthorized user, please login'
            })

        # view starts
        response = super(UserProfile, self).get(request, *args, **kwargs)
        response.data['events'] = EventListing.as_data(serializer_class=ProfileEventSerializer)(request, userprofile=request.user.id)

        return response
