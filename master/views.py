# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django_filters

from django.shortcuts import render
from rest_framework import generics
from utility import mygenerics
from django.http import JsonResponse

from serializers import AreaSerializer, CitySerializer, StateSerializer
from models import Area, City, State
from .filters import AreaFilters, AreaqpFilter

# Create your views here.
class AreaList( generics.ListAPIView, mygenerics.RelatedView ):
    serializer_class = AreaSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, AreaFilters)
    filter_class = AreaqpFilter
    queryset = Area.objects.all().order_by('name')
    pagination_class = mygenerics.NoPagination

    def get(self, request, *args, **kwargs ):
        response = super(AreaList, self).get(request, *args, **kwargs )
        return JsonResponse(data=response.data)

class CityList( generics.ListAPIView, mygenerics.RelatedView ):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    pagination_class = mygenerics.NoPagination

    def get(self, request, *args, **kwargs ):
        response = super(CityList, self).get(request, *args, **kwargs )
        return JsonResponse(data=response.data)

class StateList( generics.ListAPIView, mygenerics.RelatedView ):
    serializer_class = StateSerializer
    queryset = State.objects.all()
    pagination_class = mygenerics.NoPagination

    def get(self, request, *args, **kwargs ):
        response = super(StateList, self).get(request, *args, **kwargs )
        return JsonResponse(data=response.data)
