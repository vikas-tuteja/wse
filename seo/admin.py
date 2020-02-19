# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import MetaData
from .forms import MyModelForm

# Register your models here.

class AbsolutePathFilter(admin.SimpleListFilter):
    title = 'Absolute Path'
    parameter_name = 'abs_path'

    def lookups(self, request, model_admin):
        return [(1,'Yes'),(0,'No')]

    def queryset(self, request, queryset):
        if self.value()=='1':
            return queryset.filter(path__startswith='http://')
        else:
            return queryset


class MetaDataAdmin(admin.ModelAdmin):

    form = MyModelForm

    list_display = ('path', 'regular_expression', )
    search_fields = ('path', )
    list_filter = ('regular_expression',AbsolutePathFilter)

    class Media:
        js = (
            '/static/shared/js/jquery.js',
            '/static/admin/js/seo.js',
        )


admin.site.register(MetaData, MetaDataAdmin)
