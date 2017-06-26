from django.conf.urls import url

from views import EventListing, RequirementListing, EventDetail, ApplyForRequirement

urlpatterns = [
    url(r'^$', EventListing.as_view()),
    url(r'^requirements/(?P<event_slug>[-\w]+)/$', RequirementListing.as_view()),
    url(r'^(?P<event_slug>[-\w]+)/$', EventDetail.as_view()),
    url(r'^apply/(?P<requirement_id>[-\d]+)/$', ApplyForRequirement.as_view()),
]
