# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from datetime import datetime
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.contrib.auth.decorators import login_required

from utility import mygenerics
from rest_framework import generics
from master.views import AreaList, CityList
from rest_framework.response import Response
from filters import EventFilters, EventFilterBackend
from models import Event, Requirement, RequirementApplication, Schedule
from master.models import Area, City, HighestQualification
from utility.utils import get_prefix, getobj, slugify
from utility.restrictions import AccessToAView
from events.choices import CANDIDATE_TYPE, CANDIDATE_CLASS, GENDER
from users.models import CandidateType, LANGUAGE_PROFICIENCY
from .serializers import ListEventSerializer, ListRequirementSerializer, EventDetailSerializer, ApplyRequirementSerializer, CandidateTypeSerializer 

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
        return Event.objects.filter(schedule__start_date__gt=datetime.now().date(),show_on_site=1).\
            prefetch_related('requirement_set','schedule_set').distinct().order_by('schedule__start_date')

    def get(self, request, *args, **kwargs):
        
        response = super(EventListing, self).get(request, *args, **kwargs)

        if request.is_ajax():
            return JsonResponse( response.data )

        check = AccessToAView(self.request._request.user, 'event_listing')
        response.data['accessibility'] = True

        if not check.is_accessible():
            response.data['accessibility'] = False

        # prefix '' or '-' in sort params
        response.data['sort_order'] = get_prefix(request.GET.get('sort'))
        response.data['filters'] = request.GET.dict()
        response.data['type'] = CANDIDATE_TYPE

        return response

    
class RequirementListing( mygenerics.ListAPIView ):
    """
    Lists all requirement details of an event

    """
    serializer_class = ListRequirementSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def get_queryset(self):
        return Requirement.objects.filter(event__id=self.kwargs.get('event_id')).order_by('-id')

    
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
        return Event.objects.filter(slug=self.kwargs.get('event_slug'),id=self.kwargs.get('event_id'))

    
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


from django.contrib.auth.models import User
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
            response.data['candidate_class'] = CANDIDATE_CLASS
            response.data['gender'] = GENDER
            response.data['proficiency'] = LANGUAGE_PROFICIENCY
            response.data['education'] = HighestQualification.objects.all().values_list('slug', 'name')

        return response

    
    def post(self, request, *args, **kwargs):
        """
        input: post data of create event form
        Three step process i.e 3 tables in which data needs to be stored
        1 : events
        2 : schedules
        3 : requirements
        returns slug of the vent created

        """
        postdata = request.POST.dict()

        # step 1 : Event
        event_data = {}
        for k,v in postdata.items():
            if k in ('name', 'venue', 'briefing_venue', 'contact_person_name', 'contact_person_number', 'eligibility', 'short_description', 'payments'):
                if v:
                    event_data[k] = v

        slug = slugify(postdata['name'])
        event_data.update({
            'client' : request.user,
            'posted_by' : request.user,
            #'client' : User.objects.get(id=3),
            #'posted_by' : User.objects.get(id=3),
            'slug' : slug,
            'area' : getobj(Area, postdata['area']),
            'city' : getobj(City, postdata['city']),
        })
        if postdata['briefing_datetime']:
            event_data.update({
                'briefing_datetime' : "%s %s" % (postdata['briefing_datetime'], postdata['briefing_time'])
            })
        eventObj = Event.objects.create(**event_data)
        # TODO dump this data in logger

        # step 2 : Schedule
        contin = True
        for i in range(1,5):
            schedule_data = {}
            if contin:
                for k in ('start_date_', 'end_date_', 'start_time_', 'end_time_'):
                    key = "%s%s" % (k,i)
                    if key not in postdata or postdata.get(key) in (None, ''):
                        contin = False
                        schedule_data = None
                        break
                    else:
                        schedule_data[key[:-2]] = postdata[key]

                # TODO dump this data in logger
                if schedule_data:
                    schedule_data.update({   
                        'event' : eventObj
                    })
                    Schedule.objects.create(**schedule_data)
                    schedule_data = None


        # step 3 : Requirement
        contin = True
        for i in range(1,7):
            req_data = {}
            if contin:
                for k in ('candidate_type_', 'gender_', 'no_of_candidates_', 'daily_wage_per_candidate_', 'communication_criteria_', 'dress_code_'):
                    key = "%s%s" % (k,i)
                    if not postdata[key]:
                        contin = False
                        break
                    else:
                        req_data[key[:-2]] = postdata[key]

                if req_data:
                    req_data.update({
                        'event' : eventObj
                    })

                    candidate_type = CandidateType.objects.get(slug=postdata['candidate_type_%s' % i])
                    req_data.update({
                        'candidate_type': candidate_type
                    })

                    if postdata.get('education_%s' % i):
                        education = HighestQualification.objects.filter(slug=postdata['education_%s' % i])
                        if education:
                            req_data.update({
                                'education': education[0]
                            })

                    # TODO dump this data in logger
                    Requirement.objects.create(**req_data)
                    req_data = None


        status = True
        message = "Event created successfully. You can view it, however, it is still not on site search.<br>We will get in touch with you shortly."
        #message = "Event created successfully." 

        return JsonResponse(data={
            'status':status,
            'message':message,
            'slug':eventObj.slug,
            'id':eventObj.id
        })


# NOT NEEDED NOW, SINCE EVENT SLUG IS NO MORE UNIQUE IN THE SYSTEM
class CheckEventsExists( generics.ListAPIView ):
    """
    check in redis "key : events" if the event already exists with us
    return True if the event slug already exists, else False
    GET params : event_slug
    
    """
    serializer_class = EventDetailSerializer
    queryset = Event.objects.none()

    def get(self, request, *args, **kwargs ):

        status, message = False, str()
        event = request.GET.get('event')
        if not event:
            message = 'Invalid params: Please enter Event name'
        else:
            event_slug = slugify(event)
            con = get_redis_connection('default')
            status = con.sismember("events", event_slug)
            if status:
                message = "Error: Event by this name already exists."

        return JsonResponse(data={
            'status':status,
            'message':message,
            'slug': event_slug
        })


