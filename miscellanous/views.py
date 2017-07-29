# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from miscellanous.models import Miscellaneous
from miscellanous.serializers import FaqSerializer, AboutUsSerializer, ContactUsSerializer

# Create your views here.
class Common( generics.ListAPIView):
    queryset = Miscellaneous.objects.filter(id=1)
    serializer_class = None
    template_name = "shared/menu.html"
    
class Faqs( Common ):
    serializer_class = FaqSerializer
    template_name = "shared/faqs.html"

class ContactUs( Common ):
    serializer_class = ContactUsSerializer
    template_name = "shared/contact_us.html"

class AboutUs( Common ):
    serializer_class = AboutUsSerializer
    template_name = "shared/aboutus.html"

class Clients( Common ):
    pass

class Testimonials( Common ):
    template_name = "shared/testimonials.html"

class Articles( Common ):
    template_name = "shared/articles.html"
