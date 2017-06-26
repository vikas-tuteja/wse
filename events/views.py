# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters
from datetime import datetime
from django.shortcuts import render
from django.db import IntegrityError

from filters import EventFilters
from models import Event, Requirement, RequirementApplication
from utility import mygenerics
from rest_framework import generics
from serializers import ListEventSerializer, ListRequirementSerializer, EventDetailSerializer, ApplyRequirementSerializer 

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


class ApplyForRequirement( generics.CreateAPIView ):
    serializer_class = ApplyRequirementSerializer

    def post(self, request, *args, **kwargs):
        status = False
        reqObj = Requirement.objects.get(id=kwargs.get('requirement_id'))
        try:
            RequirementApplication.objects.create(
                requirement = reqObj,
                candidate = request.user,
                application_status = self.compute_application_status(reqObj)
            )
            status, message = True, 'Applied Successfully'
    
        except IntegrityError:
            message = 'You have already applied for this event'
        return JsonResponse(data={
            'status':status,
            'message':message
        })

    def compute_application_status(self, requirementObj):
        """
        check if this requirement is fulfilled
        return status accordingly -> applied/wl

        """
        already_applied = requirementObj.requirementapplication_set.all().count()
        if requirementObj.no_of_candidates < already_applied:
            return 'applied'
        else:
            return 'wl'
