# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Miscellaneous, Testimonial, Article

# Register your models here.
admin.site.register( Miscellaneous )
admin.site.register( Testimonial )
admin.site.register( Article )
