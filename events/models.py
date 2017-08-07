# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

from users.models import UserDetail, CandidateType 
from master.models import City, Area
from choices import *

# Create your models here.
class Event(models.Model):
    client = models.ForeignKey( User, limit_choices_to={'userdetail__type__slug' : 'client'}, related_name='client_user' )
    name = models.CharField( max_length=100 )
    slug = models.SlugField( max_length=100 )
    short_description = models.TextField( blank=True, null=True )
    overview = RichTextField( )
    venue = models.CharField( max_length=100 )
    area = models.ForeignKey( Area )
    city = models.ForeignKey( City )
    posted_by = models.ForeignKey( User, limit_choices_to = {'userdetail__type__slug__in':['client', 'cordinator']} )
    briefing_datetime = models.DateTimeField( blank=True, null=True ) 
    briefing_venue = models.CharField( max_length=100, blank=True, null=True )
    contact_person_name = models.CharField( max_length=100, blank=True, null=True )
    contact_person_number = models.BigIntegerField( blank=True, null=True)
    is_onboard = models.BooleanField( default=False )
    total_payment = models.BigIntegerField( blank=True, null=True )
    created_datetime = models.DateTimeField( auto_now_add=True )
    modify_date = models.DateTimeField( auto_now=True )
    # extra details
    eligibility = RichTextField( blank=True, null=True )
    selection_n_screening = RichTextField( blank=True, null=True )
    venue_n_timing = RichTextField( blank=True, null=True )
    payments = RichTextField( blank=True, null=True )
    t_n_c = RichTextField( blank=True, null=True )
    

    def __unicode__( self ):
       return self.name
    
    def schedule( self ):
        return (
            min([x.start_date for x in self.schedule_set.all()]),
            max([x.end_date for x in self.schedule_set.all()]),
            sum([(x.end_date - x.start_date).days + 1 for x in self.schedule_set.all()])
        )

    def shortlisted_upon_required( self ):
        return "%s / %s" % (
            len(filter( lambda z: z, 
                [y.allocationstatus_set.filter(allocation_status='shortlisted').values()
                for y in chain( *[ x.requirementapplication_set.all() for x in self.requirement_set.all()] )])),
            sum([ x.no_of_candidates for x in self.requirement_set.all()])
        )
    


class Schedule(models.Model):
    event = models.ForeignKey( Event )
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__( self ):
       return self.event.name


class Requirement(models.Model):
    event = models.ForeignKey( Event )
    candidate_type = models.ForeignKey( CandidateType )
    #work_profile = models.CharField( choices = WORK_PROFILE, max_length=255, blank=True, null=True )
    gender = models.CharField( choices = GENDER, max_length=20 )
    no_of_candidates = models.IntegerField()
    no_of_days = models.IntegerField()
    daily_wage_per_candidate = models.IntegerField()
    dress_code = models.CharField( max_length=100, blank=True, null=True )
    candidate_class = models.CharField( choices=CANDIDATE_CLASS, max_length=10, blank=True, null=True, verbose_name="class")
    communication_criteria = models.CharField( max_length=100, blank=True, null=True )

    def __unicode__( self ):
       return "%s-%s-%s-%s" % (self.event.name, self.candidate_type, self.gender, self.no_of_candidates)

    def shortlisted_upon_required( self ):
        return "%s / %s" % (
            len(filter( lambda z: z, 
                [y.allocationstatus_set.filter(allocation_status='shortlisted').values()
                for y in self.requirementapplication_set.all() ] )),
            self.no_of_candidates
        )


class RequirementApplication(models.Model):
    requirement = models.ForeignKey( Requirement )
    candidate = models.ForeignKey( User, limit_choices_to={'userdetail__type__slug' : 'candidate'} )
    application_datetime = models.DateTimeField( auto_now_add=True )
    application_status = models.CharField( choices=APPLICATION_STATUS, max_length=20 )

    def __unicode__( self ):
        return self.requirement.event.name
    
    class Meta:
        unique_together = ('requirement', 'candidate')

    def allocation_status(self):
        #import pdb; pdb.set_trace()
        #allocation_status_obj = self.allocationstatus_set.all()
        #if allocation_status_obj:
        #    return allocation_status_obj[0]
        return None

    def mobile(self):
        return self.candidate.userdetail.mobile


class AllocationStatus(models.Model):
    application = models.ForeignKey( RequirementApplication )
    allocation_datetime = models.DateTimeField( auto_now_add=True )
    allocation_status = models.CharField( choices=ALLOCATION_STATUS, max_length=50 )

    def __unicode__( self ):
        return self.allocation_status
