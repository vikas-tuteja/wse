from django.conf.urls import url

from views import EventListing, RequirementListing, EventDetail, ApplyForRequirement

urlpatterns = [
    url(r'^$', EventListing.as_view(), name="event_listing"),
    url(r'^requirements/(?P<event_slug>[-\w]+)/$', RequirementListing.as_view(), name="requirement_listing"),
    url(r'^(?P<event_slug>[-\w]+)/$', EventDetail.as_view(), name="event_slug"),
    url(r'^apply/(?P<requirement_id>[-\d]+)/$', ApplyForRequirement.as_view(), name="event_apply"),
]
