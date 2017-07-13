from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class BaseMiddleware(MiddlewareMixin):
    """
    Add MEDIA_URL + user detials to the response dictionary

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
        if response.status_code == 200 and "/admin/" not in request.path :
            response.data['STATIC_URL'] = settings.STATIC_URL

        return response
