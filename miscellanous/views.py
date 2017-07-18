# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from users.models import UserDetail
from users.serializers import UserSerializer

# Create your views here.
class Common( generics.ListAPIView):
    queryset = UserDetail.objects.none()
    serializer_class = UserSerializer
    template_name = "shared/menu.html"
    
class Faqs( Common ):
    pass

class Articles( Common ):
    pass

class Clients( Common ):
    pass

class Testimonials( Common ):
    pass

class ContactUs( Common ):
    pass
