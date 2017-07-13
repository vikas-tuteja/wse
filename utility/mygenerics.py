from rest_framework import mixins, generics

class FormatResponse(object):

    def get_response(self, response, *args, **kwargs):
        response.data = {
            'results': response.data,
            'count': len(response.data)
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
