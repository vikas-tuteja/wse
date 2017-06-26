# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import * 

# Register your models here.
class RequirementApplicationAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'candidate', 'allocation_datetime', 'application_status')


class ScheduleAdminInline(admin.StackedInline):
    model = Schedule
    extra = 1
    min_num = 1

class RequirementsAdminInline(admin.StackedInline):
    list_display = ('event', 'candidate_type', 'gender', 'no_of_candidates', 'no_of_days', 'daily_wage_per_candidate')
    model = Requirement
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'venue', 'city']
    inlines = ( ScheduleAdminInline, RequirementsAdminInline, )


admin.site.register(Event, EventAdmin)
admin.site.register(AllocationStatus)
admin.site.register(RequirementApplication, RequirementApplicationAdmin)
