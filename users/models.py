# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from master.models import State, City


# Create your models here.
class UserRole(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name


class User(models.Model):
    auth_user = models.ForeignKey( User )
    type = models.ForeignKey( UserRole )
    mobile = models.BigIntegerField()
    address	= models.CharField( max_length=100 )
    city = models.ForeignKey( City )
    state = models.ForeignKey( State )
    created_date = models.DateTimeField( auto_now_add=True )
    modified_date = models.DateTimeField( auto_now=True )
    is_paid	= models.BooleanField(default=False)
    paid_from_date = models.DateTimeField( blank=True, null=True )
    paid_till_date = models.DateTimeField( blank=True, null=True )

    def __unicode__( self ):
       return self.auth_user.username
    
    class Meta:
        verbose_name = "Users extra detail"


class Client(models.Model):
    user = models.ForeignKey( User )
    company_name = models.CharField( max_length=100, blank=True, null=True )
    company_address = models.CharField( max_length=100, blank=True, null=True )
    establishment_year = models.IntegerField( blank=True, null=True )

    def __unicode__( self ):
       return self.user.auth_user.username

    class Meta:
        verbose_name = "Client extra information"
