# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Miscellaneous( models.Model ):
    faq_content = RichTextField() 
    aboutus_content = RichTextField() 
    contactus_content = RichTextField() 
    tnc = RichTextField()
    privacypolicy = RichTextField()


class CommonPublish( models.Model ):
    user = models.ForeignKey( User )
    title = models.CharField( max_length=200 )
    content = RichTextField()
    show_on_site = models.BooleanField(default=False)

    def __unicode__( self ):
       return "%s -by %s" % (self.title, self.user.username)

class Testimonial( CommonPublish ):
    pass

class Article( CommonPublish ):
    pass
