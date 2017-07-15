from rest_framework import mixins, generics
from django.db import models
from rest_framework.response import Response

class FormatResponse(object):

    def get_response(self, response, *args, **kwargs):
        response.data = {
            'results': response.data,
        }
        return response


class ListAPIView(FormatResponse,
                  mixins.ListModelMixin,
                  generics.GenericAPIView):
    """
    Concrete view for listing a queryset.
    """
    def get(self, request, *args, **kwargs):
        return super(ListAPIView, self).get_response(self.list(request, *args, **kwargs))



AS_MAIN=1
class RelatedView(object):
    '''View class makes a view callable from other view. '''
    relview = None
    jointrel = None
    @classmethod
    def as_data(cls,**initkwargs):
        def view(request,*args,**kwargs):
            self=cls(**initkwargs)
            self.retType = 'data'
            self.request = request
            self.format_kwarg = None
            self.args = args
            self.kwargs = kwargs
            resp =  self.get(request,*args,**kwargs)
            if isinstance(resp,Response):resp = resp.data
            return resp

        setattr(view,'__name__',cls.__name__)
        setattr(view,'_class',cls)
        setattr(view,'_initkwargs',initkwargs)
        return view


class NoPagination(object):
    """ 
    Wraps data wrapped in a dict with key name 'results'.Return Response object.
    Use with pagination_class=NoPagination as view attribute 
    """
    display_page_controls = False
    def paginate_queryset(self,queryset,request,view=None):
        if isinstance(queryset,models.Manager):
            queryset=queryset.all()
        return list(queryset)

    def get_paginated_response(self,data):
        return Response({'results':data})

    def get_results(self, data):
        return data['results']
