# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Miscellaneous( models.Model ):
    faq_content = RichTextField() 
    aboutus_content = RichTextField() 
    contactus_content = RichTextField() 
