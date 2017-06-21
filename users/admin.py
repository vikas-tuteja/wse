# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import User, UserRole, Client

# Register your models here.
class ClientAdminInline(admin.StackedInline):
    model = Client
    extra = 1
    max_num = 1


class UsersAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'city', 'state', 'created_date', 'is_paid']
    inlines = (ClientAdminInline,)



admin.site.register( UserRole )
admin.site.register( User, UsersAdmin )
