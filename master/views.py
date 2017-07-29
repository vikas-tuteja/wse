# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from utility import mygenerics
from django.http import JsonResponse

from serializers import AreaSerializer
from models import Area

# Create your views here.
class AreaList( generics.ListAPIView, mygenerics.RelatedView ):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    pagination_class = mygenerics.NoPagination

    def get(self, request, *args, **kwargs ):
        response = super(AreaList, self).get(request, *args, **kwargs )
        return JsonResponse(data=response.data)
