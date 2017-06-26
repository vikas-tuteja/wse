# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from django.contrib.auth.models import User


from serializers import UserSerializer
from models import UserDetail

# Create your views here.

class CreateUser( generics.CreateAPIView ):
    pass

class LoginUser( generics.ListAPIView ):
    pass

class ChangePassword( generics.UpdateAPIView ):
    """
    this will change the password of the user to 
    his/her 10 digit mobile number

    """
    serializer_class = UserSerializer
    queryset = UserDetail.objects.all()
    lookup_field = "auth_user__email"
    lookup_url_kwarg = "user_email"

    def put(self, request, *args, **kwargs):
        status = False
        import pdb; pdb.set_trace()
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
