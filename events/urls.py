from django.conf.urls import url

from views import EventListing

urlpatterns = [
    url(r'^$', EventListing.as_view())
]
