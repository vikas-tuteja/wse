# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import State, City, Area


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']

class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'city' ]

admin.site.register( State )
admin.site.register( City, CityAdmin )
admin.site.register( Area, AreaAdmin )
