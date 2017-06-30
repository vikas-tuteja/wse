# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from models import * 
from choices import ALLOCATION_STATUS

from django.contrib.admin.helpers import ActionForm
# ActionForm is the default form used by Django
# You can extend this class

class AllocationStatusForm(ActionForm):
    allocation_status = forms.ChoiceField( choices=ALLOCATION_STATUS, required=True, label='select allocation status' )

# Register your models here.
def bulk_update_allocation_status_for_candidates(modeladmin, request, queryset):
    for each_req_app_obj in queryset:
        allocation_status_obj = each_req_app_obj.allocationstatus_set.all()
        # create new
        if not allocation_status_obj:
            AllocationStatus.objects.create(
                application = each_req_app_obj,
                allocation_status = request.POST['allocation_status'] 
            )
        # update existing's status
        else:
            allocation_status_obj.update(
                allocation_status = request.POST['allocation_status']
            )

class RequirementApplicationAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'candidate', 'application_datetime', 'application_status', 'allocation_status')
    search_fields = ('requirement__event__name', )
    action_form = AllocationStatusForm
    actions = [bulk_update_allocation_status_for_candidates]


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
admin.site.register(RequirementApplication, RequirementApplicationAdmin)
admin.site.register(AllocationStatus)
