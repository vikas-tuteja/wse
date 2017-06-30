# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate

from serializers import UserSerializer, AuthUserSerializer
from models import UserDetail, UserRole

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
    
    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()

    def post(self, request, *args, **kwargs):
        status = False
        kwargs.update(request.POST.dict())
        
        # check if user already exists
        email = kwargs.get('email')
        mobile = kwargs.get('mobile')[-10:]
        exists = UserDetail.objects.filter(
            Q(auth_user__email=email) | Q(mobile=mobile)
        )

        if not exists:
            try:
                # create auth user first
                auth_user = User.objects.create(
                    username = email,
                    email = email,
                )
                auth_user.set_password(kwargs.get('password'))
                auth_user.save()
                
                # then create userdetails
                user_detail = UserDetail.objects.create(
                    auth_user = auth_user,
                    type = UserRole.objects.get(slug=kwargs.get('user_role')),
                    mobile = mobile,
                )
                user_detail.save()

                status = True
                message = 'User created successfully'

            except IntegrityError:
                message = 'User with this email or mobile already exists '
        else:
            message = 'User with this email or mobile already exists '

        return JsonResponse(data={
            'status':True,
            'message':message
        })
        

class LoginUser( generics.ListAPIView ):
    """
    METHOD : POST
    POST PARAMS: email
               : password
    """
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()
    
    def post(self, request, *args, **kwargs):
        kwargs.update(request.POST.dict())
        status = False
        user = authenticate( 
            username = kwargs.get('email'),
            password = kwargs.get('password')
        )

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
    #lookup_field = "auth_user__email"
    #lookup_url_kwarg = "user_email"

    def put(self, request, *args, **kwargs):
        status = False
        email = request.POST.get('email')
        if not email:
            message = 'Error: Please enter email id.'

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
    queryset = UserDetail.objects.all()
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


# TODO 
# ajax request to check user availibilty, will use redis for this
# event allocation status ADMIN for mehul, with multi select status update actions
# seo meta backend
