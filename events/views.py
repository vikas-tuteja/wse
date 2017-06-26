# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters
from datetime import datetime
from django.shortcuts import render

from filters import EventFilters
from models import Event, Requirement
from utility import mygenerics
from serializers import ListEventSerializer, ListRequirementSerializer, EventDetailSerializer


# Create your views here.
class EventListing( mygenerics.ListAPIView ):
    """
    As the name says, lists all Events
    GET PARAMS: filters will be applied

    """
    serializer_class = ListEventSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = EventFilters

    def get_queryset(self):
        # get events starting from tomorrow order by datetime
        # since cannot apply on same date of event.
        return Event.objects.filter(schedule__start_date__gt=datetime.now().\
            date()).prefetch_related('requirement_set').distinct().order_by('id')

    
    def list(self, request, *args, **kwargs):
        response = super(EventListing, self).list(request, *args, **kwargs)
        return response
    
    
class RequirementListing( mygenerics.ListAPIView ):
    """
    Lists all requirement details of an event

    """
    serializer_class = ListRequirementSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        return Requirement.objects.filter(event__slug=self.kwargs.get('event_slug')).order_by('-id')

    
    def list(self, request, *args, **kwargs):
        response = super(RequirementListing, self).list(request, *args, **kwargs)
        return response


class EventDetail( mygenerics.ListAPIView ):
    """
    Entire Details of an event
    
    """
    serializer_class = EventDetailSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        return Event.objects.filter(slug=self.kwargs.get('event_slug'))

    
    def list(self, request, *args, **kwargs):
        response = super(EventDetail, self).list(request, *args, **kwargs)
        return response
