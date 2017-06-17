# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import State, City


# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'state']

admin.site.register( State )
admin.site.register( City, CityAdmin )
