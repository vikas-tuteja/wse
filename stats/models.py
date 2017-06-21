# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from users.models import User
from events.models import Event
from events.choices import EVENT_STATUS

# Create your models here.
class EventStat(models.Model):
    event = models.ForeignKey( Event )
    status = models.CharField( choices = EVENT_STATUS, max_length=20 )
    viewed = models.IntegerField()
    interested = models.IntegerField()
    remarks = models.CharField( max_length=100 )

    def __unicode__( self ):
       return self.status


class CordinatorStat(models.Model):
    cordinator = models.ForeignKey( User, limit_choices_to={'type__slug':'cordinator'} )
    event  = models.ForeignKey( Event )

    def __unicode__( self ):
       return self.event


class CandidateStat(models.Model):
    candidate = models.ForeignKey( User, limit_choices_to={'type__slug':'candidate'})
    event = models.ForeignKey( Event )

    def __unicode__( self ):
       return self.event

