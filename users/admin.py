# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import User, UserRole, Client, Cordinator, Candidate
# Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'city', 'state', 'created_date', 'is_paid']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name']


admin.site.register( UserRole )
admin.site.register( User, UsersAdmin )
admin.site.register( Client, ClientAdmin )
admin.site.register( Cordinator )
admin.site.register( Candidate )
