# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from users.models import User 
from master.models import City
from choices import CANDIDATE_TYPE, GENDER, CANDIDATE_CLASS

# Create your models here.
class Event(models.Model):
    client = models.ForeignKey( User, limit_choices_to={'type__slug' : 'client'}, related_name='client_user' )
    name = models.CharField( max_length=100 )
    description = models.CharField( max_length=100 )
    venue = models.CharField( max_length=100 )
    city = models.ForeignKey( City )
    event_posted_by = models.ForeignKey( User, limit_choices_to = {'type__slug__in':['client', 'cordinator']} )
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()
    notes = models.TextField( blank=True, null=True )
    briefing_datetime = models.DateTimeField( blank=True, null=True ) 
    briefing_venue = models.CharField( max_length=100, blank=True, null=True )
    contact_person_name = models.CharField( max_length=100, blank=True, null=True )
    contact_person_number = models.BigIntegerField( blank=True, null=True)
    #TODO :  make a decision: if we need this column: 
    # bcoz the oe who posts the event, will make the payment,
    # hence, we dont need payment_made_by column
    # define whether cordinator or client or both can make payment.
    #payment_made_by = models.ForeignKey( User, blank=True, null=True )
    total_payment = models.BigIntegerField( blank=True, null=True )

    def __unicode__( self ):
       return self.name


class EventsRequirement(models.Model):
    event = models.ForeignKey( Event )
    candidate_type = models.CharField( choices = CANDIDATE_TYPE, max_length=20 )
    work_profile = models.CharField( max_length=255, blank=True, null=True )
    gender = models.CharField( choices = GENDER, max_length=20 )
    no_of_candidates = models.IntegerField()
    no_of_days = models.IntegerField()
    daily_wage_per_candidate = models.IntegerField()
    dress_code = models.CharField( max_length=100, blank=True, null=True )
    candidate_class = models.CharField( choices=CANDIDATE_CLASS, max_length=10, blank=True, null=True, verbose_name="class")
    communication_criteria = models.CharField( max_length=100, blank=True, null=True )

    def __unicode__( self ):
       return self.event
