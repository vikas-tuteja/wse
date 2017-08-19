# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from datetime import datetime
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from filters import EventFilters, EventFilterBackend
from models import Event, Requirement, RequirementApplication
from utility import mygenerics
from rest_framework import generics
from rest_framework.response import Response
from serializers import ListEventSerializer, ListRequirementSerializer, EventDetailSerializer, ApplyRequirementSerializer, CandidateTypeSerializer 
from master.views import AreaList, CityList
from utility.utils import get_prefix
from utility.restrictions import AccessToAView
from events.choices import CANDIDATE_TYPE, CANDIDATE_CLASS, GENDER
from users.models import CandidateType

# Create your views here.
class EventListing( generics.ListAPIView, mygenerics.RelatedView ):
    """
    As the name says, lists all Events
    GET PARAMS: filters will be applied

    """
    serializer_class = ListEventSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, EventFilterBackend)
    filter_class = EventFilters
    template_name = 'events/listing_base.html'
    related_views = {
        'area': (AreaList.as_data(), '*', 1),
    }

    def get_queryset(self):
        # get events starting from tomorrow order by datetime
        # since cannot apply on same date of event.
        return Event.objects.filter(schedule__start_date__gt=datetime.now().\
            date()).prefetch_related('requirement_set').distinct().order_by('id')

    def get(self, request, *args, **kwargs):
        
        response = super(EventListing, self).get(request, *args, **kwargs)

        check = AccessToAView(self.request._request.user, 'event_listing')
        response.data['accessibility'] = True

        if not check.is_accessible():
            response.data['accessibility'] = False

        # prefix '' or '-' in sort params
        response.data['sort_order'] = get_prefix(request.GET.get('sort'))
        response.data['filters'] = request.GET.dict()
        response.data['type'] = CANDIDATE_TYPE

        if request.is_ajax():
            return JsonResponse( response.data )

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
    template_name = 'events/details_base.html'
    pagination_class = None

    def get_queryset(self):
        return Event.objects.filter(slug=self.kwargs.get('event_slug'))

    
    def list(self, request, *args, **kwargs):
        response = super(EventDetail, self).list(request, *args, **kwargs)

        check = AccessToAView(self.request._request.user, 'event_detail')
        response.data[0]['accessibility'] = True

        if not check.is_accessible():
            response.data[0]['accessibility'] = False

        return response


class ApplyForRequirement( generics.CreateAPIView ):
    serializer_class = ApplyRequirementSerializer

    def get(self, request, *args, **kwargs):
        status = False
        check = AccessToAView(self.request._request.user, 'apply_requirement')
 
        if not check.is_accessible():
            message = 'Unauthorized Access: Only candidates can Apply and Work for an event. Please Login as a Candidate'

        else:
            reqObj = Requirement.objects.get(id=kwargs.get('requirement_id'))
            try:
                RequirementApplication.objects.create(
                    requirement = reqObj,
                    candidate = request.user,
                    application_status = self.compute_application_status(reqObj)
                )
                status, message = True, 'Applied Successfully! We will get in touch with you shortly.'
        
            except IntegrityError:
                message = 'Error: You have already applied for this event.'

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
        if requirementObj.no_of_candidates != already_applied:
            return 'applied'
        else:
            return 'wl'


                
class CandidateTypeList( generics.ListAPIView, mygenerics.RelatedView ):   
    serializer_class = CandidateTypeSerializer                             
    queryset = CandidateType.objects.all() 
    pagination_class = mygenerics.NoPagination                             
                                                                           
    def get(self, request, *args, **kwargs):
        response = super(CandidateTypeList, self).get(request, *args, **kwargs )    
        return JsonResponse(data=response.data)


class PostEvents( generics.ListAPIView ):
    """
    get : gives post event form
    post: creates event with show on site off

    """
    queryset = Event.objects.none()
    serializer_class = EventDetailSerializer
    template_name = "events/post_events_base.html"
    # select box meta data
    related_views = {
        'area': (AreaList.as_data(), '*', 1),
        'city': (CityList.as_data(), '*', 1),
        'candidate_type': (CandidateTypeList.as_data(), '*', 1),
    }

    def get(self, *args, **kwargs):
        check = AccessToAView(self.request._request.user, 'post_events')
        response = super(PostEvents, self).get(*args, **kwargs)
        response.data['accessibility'] = True

        if not check.is_accessible():
            response.data['accessibility'] = False

        else:
            # TODO create an event form
            response.data['candidate_class'] = CANDIDATE_CLASS
            response.data['gender'] = GENDER

        return response

    
    def post(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        # <QueryDict: {u'post_events_1[area]': [u'chembur'], u'post_events_2[selection_n_screening]': [u'ghjhgfcvbn'], u'post_events_1[city]': [u'mumbai'], u'post_events_3[gender_1]': [u'm'], u'post_events_3[candidate_type_1]': [u'promotor'], u'post_events[tnc_1]': [u'on'], u'post_events_1[contact_person_number]': [u'9876543211'], u'post_events_2[venue_n_timing]': [u'bvbn'], u'post_events_2[payments]': [u'bvbnm'], u'post_events[tnc_2]': [u'on'], u'post_events_1[name]': [u'testing event 1'], u'post_events_1[venue]': [u'k-star'], u'post_events_2[description]': [u'some random description'], u'post_events_2[eligibility]': [u'chjhgfcf']}>

        status = True
        message = "Event created successfully. However, it is still not on site.<br>We will get in touch with you shortly."
        message = "Event created successfully." 

        return JsonResponse(data={
            'status':status,
            'message':message
        })


