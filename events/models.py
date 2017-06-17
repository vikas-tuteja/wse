# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from users.models import Client
from master.models import City
from choices import CANDIDATE_TYPE, EVENT_STATUS

# Create your models here.
class Event(models.Model):
    client = models.ForeignKey( Client )
    name = models.CharField( max_length=100 )
    description = models.CharField( max_length=100 )
    venue = models.CharField( max_length=100 )
    city = models.ForeignKey( City )
    event_start_datetime = models.DateTimeField()
    event_end_datetime = models.DateTimeField()

    def __unicode__( self ):
       return self.name


class EventsRequirement(models.Model):
    event = models.ForeignKey( Event )
    candidate_type = models.CharField( choices = CANDIDATE_TYPE, max_length=20 )
    no_of_male_candidates = models.IntegerField()
    no_of_female_candidates = models.IntegerField()

    def __unicode__( self ):
       return self.event
