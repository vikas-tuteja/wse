# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import User, UserRole, ClientAttribute, CordinatorAttribute, CandidateAttribute, CandidateType

# Register your models here.
class ClientAdminInline(admin.StackedInline):
    model = ClientAttribute
    extra = 1
    max_num = 1


class CordinatorAdminInline(admin.StackedInline):
    model = CordinatorAttribute
    extra = 1
    max_num = 1


class CandidateAdminInline(admin.StackedInline):
    model = CandidateAttribute
    filter_horizontal = ('candidate_profile',)
    extra = 1
    max_num = 1


class UsersAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'type', 'mobile', 'blacklist_flag']
    inlines = (ClientAdminInline, CordinatorAdminInline, CandidateAdminInline)


admin.site.register( UserRole )
admin.site.register( CandidateType )
admin.site.register( User, UsersAdmin )
