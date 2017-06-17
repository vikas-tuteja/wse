# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import * 

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'venue', 'city', 'event_start_datetime', 'event_end_datetime']


class EventsRequirementAdmin(admin.ModelAdmin):
    list_display = ['event', 'candidate_type', 'no_of_male_candidates', 'no_of_female_candidates']


admin.site.register(Event, EventAdmin)
admin.site.register(EventsRequirement, EventsRequirementAdmin)
