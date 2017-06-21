# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters
from django.shortcuts import render

from models import Event
from rest_framework import generics
from serializers import ListEventSerializer
from filters import EventFilters


# Create your views here.
class EventListing( generics.ListAPIView ):

    serializer_class = ListEventSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = EventFilters

    def get_queryset(self):
        return Event.objects.all().prefetch_related('eventsrequirement_set').order_by('event_start_datetime')

    
    def list(self, request, *args, **kwargs):
        response = super(EventListing, self).list(request, *args, **kwargs)
        return response
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
