# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import urlresolvers
from django.http import JsonResponse


# Create your views here.
def get_named_url_list(request):
    """
    Returns a pattern dictionary with key as name of the named urls and value as its
    corresponding regex.

    """
    root_url_resolver = 'wse.urls'
    resolver = urlresolvers.get_resolver(root_url_resolver)
    pattern_list = sorted([(k, value[1]) for k, value in resolver.reverse_dict.items() if isinstance(k, basestring)])

    return JsonResponse(data={
        'results':pattern_list
    })
