# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import * 

# Register your models here.

class RequirementsAdminInline(admin.StackedInline):
    model = Requirement
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'venue', 'city']
    inlines = ( RequirementsAdminInline, )


admin.site.register(Event, EventAdmin)
admin.site.register(RequirementAllocation)
admin.site.register(AllocationStatus)
