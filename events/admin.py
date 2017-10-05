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
        # TODO verify before shortlisting, that number of shortlisting candidates of req. X < no of candidates required for req. X
        # if not dont allow to change allocation status
        if True:
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
    list_display = ('requirement', 'candidate', 'application_datetime', 'application_status', 'mobile', 'allocation_status', 'event_page', 'user_page')
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
    search_fields = ('name',)
    list_display = ['name', 'venue', 'show_on_site', 'created_datetime', '__schedule__', 'shortlisted_upon_required', 'client']
    inlines = ( ScheduleAdminInline, RequirementsAdminInline, )

    def __schedule__(self, obj):
        data = obj.schedule()
        return "From %s To %s (%s days) " % data


class RequirmentAdmin(admin.ModelAdmin):
    list_display = ('event', 'candidate_type', 'gender', 'shortlisted_upon_required')
    search_fields = ('event__name', )
    def has_add_permission(self, obj):
        return False
    
    
admin.site.register(Event, EventAdmin)
admin.site.register(RequirementApplication, RequirementApplicationAdmin)
admin.site.register(Requirement, RequirmentAdmin)
