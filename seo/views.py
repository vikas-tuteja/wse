# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core import urlresolvers


# Create your views here.
def get_named_url_list(request):
    """
    Returns a pattern dictionary with key as name of the named urls and value as its
    corresponding regex.
    """

    subdomain = request.GET.get('mobile','www')

    root_url_resolver = 'wse.urls'
    resolver = urlresolvers.get_resolver(root_url_resolver)
    pattern_list = sorted([value[1] for key, value in resolver.reverse_dict.items() if isinstance(key, basestring)])

    return render_to_response('seo/get_named_url_list.html', locals())
