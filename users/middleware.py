import json
from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.urlresolvers import resolve

from seo.models import MetaData


class BaseMiddleware(MiddlewareMixin):
    """
    Add MEDIA_URL + user detials to the response dictionary
    Add related views to the result dict

    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_template_response(self, request, response):
        if response.status_code == 200 and "/admin/" not in request.path:
            # append static url in the response
            response.data['STATIC_URL'] = settings.STATIC_URL

            # append seo meta in views other than admin
            url_name = resolve(request.path).url_name
            obj = MetaData.objects.filter(path=url_name)
            if obj:
                obj = obj[0]
                meta = {
                    'title':obj.title,
                    'keywords':obj.keywords,
                    'description':obj.description,
                }
                response.data['meta'] = meta


        # calling related views of a view
        try:
            related_views = request.resolver_match.func.cls.related_views
            for key, func in related_views.items():
                try:
                    response.data[key] = json.loads(func[0](func[1])._container[0])['results']
                except:
                    response.data[key] = None
        except:
            pass

        return response
