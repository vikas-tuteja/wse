# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from datetime import datetime
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from filters import EventFilters, EventFilterBackend
from models import Event, Requirement, RequirementApplication, Schedule
from utility import mygenerics
from rest_framework import generics
from rest_framework.response import Response
from serializers import ListEventSerializer, ListRequirementSerializer, EventDetailSerializer, ApplyRequirementSerializer, CandidateTypeSerializer 
from master.views import AreaList, CityList
from master.models import Area, City
from utility.utils import get_prefix, getobj, slugify
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
            # TODO create an event form
            response.data['candidate_class'] = CANDIDATE_CLASS
            response.data['gender'] = GENDER

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
        postdata = {u'no_of_candidates_6': u'', u'no_of_candidates_5': u'', u'end_time_1': u'17:00', u'no_of_candidates_3': u'', u'contact_person_name': u'', u'communication_criteria1': u'm', u'communication_criteria6': u'', u'dress_code_2': u'', u'communication_criteria5': u'', u'dress_code_3': u'', u'start_date_1': u'2017-09-02', u'communication_criteria4': u'', u'daily_wage_per_candidate_1': u'500', u'venue': u'Inorbit Mall', u'briefing_datetime': u'', u'communication_criteria3': u'', u'briefing_venue': u'', u'dress_code_1': u'', u'no_of_candidates_2': u'', u'start_time_1': u'11:00', u'city': u'mumbai', u'daily_wage_per_candidate_4': u'', u'no_of_candidates_1': u'5', u'area': u'chembur', u'no_of_candidates_4': u'', u'field7': u'on', u'dress_code_4': u'', u'eligibility': u'', u'candidate_type_2': u'', u'venue_n_timing': u'', u'short_description': u'jhgfdfgh', u'contact_person_number': u'9876543211', u'payments': u'hgfdfghjk', u'education_1': u'', u'education_2': u'', u'education_3': u'', u'education_4': u'', u'education_5': u'', u'education_6': u'', u'gender_6': u'', u'briefing_time': u'', u'gender_4': u'', u'gender_5': u'', u'gender_2': u'', u'gender_3': u'', u'gender_1': u'm', u'communication_criteria2': u'', u'no_of_days_1': u'5', u'daily_wage_per_candidate_2': u'', u'selection_n_screening': u'', u'end_date_1': u'2017-09-09', u'name': u'third event from ui', u'no_of_days_2': u'', u'candidate_type_3': u'', u'daily_wage_per_candidate_6': u'', u'daily_wage_per_candidate_5': u'', u'dress_code_5': u'', u'daily_wage_per_candidate_3': u'', u'candidate_type_6': u'', u'candidate_type_5': u'', u'candidate_type_4': u'', u'no_of_days_6': u'', u'dress_code_6': u'', u'no_of_days_4': u'', u'no_of_days_5': u'', u'tnc_1': u'on', u'no_of_days_3': u'', u'tnc_2': u'on', u'candidate_type_1': u'promotor'}

        # step 1 : Event
        event_data = {}
        for k,v in postdata.items():
            if k in ('name', 'venue', 'briefing_venue', 'contact_person_name', 'contact_person_number', 'eligibility', 'selection_n_screening', 'venue_n_timing', 'short_description'):
                if v:
                    event_data[k] = v

        slug = slugify(postdata['name'])
        event_data.update({
            #'client' : request.user,
            'client' : User.objects.get(id=3),
            'slug' : slug,
            'area' : getobj(Area, postdata['area']),
            'city' : getobj(City, postdata['city']),
            #'posted_by' : request.user,
            'posted_by' : User.objects.get(id=3),
        })
        if postdata['briefing_datetime']:
            event_data.update({
                'briefing_datetime' : postdata['briefing_datetime'] + postdata['briefing_time']
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
                    if key not in postdata:
                        contin = False
                        break
                    else:
                        schedule_data[key[:-2]] = postdata[key]

                # TODO dump this data in logger
                print schedule_data
                import pdb; pdb.set_trace()
                if bool(schedule_data):
                    schedule_data.update({   
                        'event' : eventObj
                    })
                Schedule.objects.create(**schedule_data)
                schedule_data = None


        # step 3 : Requirement
        contin = True
        for i in range(1,7):
            req_data = {
                'event' : eventObj
            }
            if contin:
                for k in ('candidate_type_', 'gender_', 'no_of_candidates_', 'no_of_days_', 'daily_wage_per_candidate_', 'education_'):
                    key = "%s%s" % (k,i)
                    if key not in postdata:
                        contin = False
                        break
                    else:
                        req_data[key[:-2]] = postdata[key]

                # TODO dump this data in logger
                Requirement.objects.create(**req_data)


        status = True
        message = "Event created successfully. However, it is still not on site.<br>We will get in touch with you shortly."
        message = "Event created successfully." 

        return JsonResponse(data={
            'status':status,
            'message':message
        })


