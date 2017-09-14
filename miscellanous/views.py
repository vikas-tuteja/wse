# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics

from miscellanous.models import Miscellaneous, Testimonial, Article
from miscellanous.serializers import FaqSerializer, AboutUsSerializer, ContactUsSerializer, TestimonialsSerializer, ArticleSerializer, TNCSerializer

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

class Testimonials( generics.ListAPIView ):
    serializer_class = TestimonialsSerializer
    queryset = Testimonial.objects.filter(show_on_site=1).distinct()
    template_name = "shared/testimonials.html"

class Articles( generics.ListAPIView ):
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(show_on_site=1)
    template_name = "shared/articles.html"

class TNC( Common ):
    serializer_class = TNCSerializer
    template_name = "shared/tnc.html"
