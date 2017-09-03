# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django_redis import get_redis_connection

from master.models import Area, State, City, HighestQualification
from choices import *

def uploadpath(instance, filename):
    """ Computes the user image upload path """
    try:
        data_model = "%s" % instance.auth_user.username
    except:
        data_model = "%s" % str(instance.id)
    return "uploads/profile/%s/%s" % (data_model, filename.replace(' ', '-'))


# Create your models here.
class UserRole(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name


class CandidateType(models.Model):
    name = models.CharField( max_length=50 )
    slug = models.SlugField( max_length=50 )

    def __unicode__(self):
        return self.name


class UserDetail(models.Model):
    auth_user = models.OneToOneField( User )
    type = models.ForeignKey( UserRole )
    mobile = models.BigIntegerField( unique=True )
    whatsapp_number = models.BigIntegerField( blank=True, null=True )
    address	= models.CharField( max_length=100, blank=True, null=True )
    image = models.ImageField( upload_to=uploadpath, blank=True, null=True )
    area = models.ForeignKey( Area, blank=True, null=True )
    city = models.ForeignKey( City, blank=True, null=True )
    state = models.ForeignKey( State, blank=True, null=True )
    highest_qualification = models.ForeignKey( HighestQualification, blank=True, null=True ) 
    blacklist_flag = models.IntegerField( default=0 )

    def __unicode__( self ):
       return self.auth_user.username
    
    class Meta:
        verbose_name = "Create / Modify User"

    def save(self, *args, **kwargs):
        # Add new username to redis set of usernames
        if not self.id:
            con = get_redis_connection('default')
            con.sadd("usernames", self.auth_user.username)
        return super(UserDetail, self).save(*args, **kwargs)


class ClientAttribute(models.Model):
    user = models.ForeignKey( UserDetail )
    designation = models.CharField ( max_length=100, blank=True, null=True )
    company_name = models.CharField( max_length=100, blank=True, null=True )
    company_address = models.CharField( max_length=100, blank=True, null=True )
    establishment_year = models.IntegerField( blank=True, null=True )

    def __unicode__( self ):
       return self.user.auth_user.username

    class Meta:
        verbose_name = "Client Attributes (to be filled only if user type is client)"


class CordinatorAttribute(models.Model):
    user = models.ForeignKey( UserDetail )
    working_for = models.CharField( choices=CORDINATOR_WORKING_FOR, max_length=50, blank=True, null=True  )

    def __unicode__( self ):
       return self.user.auth_user.username

    class Meta:
        verbose_name = "Cordinator Attributes (to be filled only if user type is cordinator)"


class CandidateAttribute(models.Model):
    user = models.ForeignKey( UserDetail )
    # TODO Not able to save below field
    language_proficiency = models.CharField( choices=LANGUAGE_PROFICIENCY, max_length=50, blank=True, null=True ) 
    looks = models.CharField( choices=LOOKS, max_length=50, blank=True, null=True ) 
    open_to_which_kind_of_job = models.CharField( max_length=100, blank=True, null=True, verbose_name="Open to which kind of jobs / workprofiles" )
    pay_scale = models.CharField( max_length=100, blank=True, null=True )
    comfortable_travelling_outdoor = models.IntegerField( default= False )
    comfortable_for_liquor_promotion = models.IntegerField( default= False )
    comfortable_working_at_odd_timings = models.IntegerField( default= False )
    candidate_profile = models.ManyToManyField( CandidateType )

    def __unicode__( self ):
       return self.user.auth_user.username

    class Meta:
        verbose_name = "Candidate Attributes (to be filled only if user type is cordinator)"
