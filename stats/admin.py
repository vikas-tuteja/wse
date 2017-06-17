# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import *

# Register your models here.
class EventStatAdmin(admin.ModelAdmin):
    list_display = ['event', 'status', 'viewed', 'interested', 'remarks']


class CordinatorStatAdmin(admin.ModelAdmin):
    list_display = ['cordinator', 'event']


class CandidateStatAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'event' ]


admin.site.register(EventStat, EventStatAdmin)
admin.site.register(CordinatorStat, CordinatorStatAdmin)
admin.site.register(CandidateStat, CandidateStatAdmin)
