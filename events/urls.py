from django.conf.urls import url

from views import EventListing, RequirementListing, EventDetail, ApplyForRequirement

urlpatterns = [
    # event listing urls
    url(r'^events/$', EventListing.as_view(), name="event_listing"),
    url(r'^events-in-(?P<city_slug>[-\w]+)-city/$', EventListing.as_view(), name="event_listing"),
    url(r'^events-in-(?P<area_slug>[-\w]+)/$', EventListing.as_view(), name="event_listing"),

    # other
    url(r'^events/requirements/(?P<event_slug>[-\w]+)/$', RequirementListing.as_view(), name="requirement_listing"),
    url(r'^events/(?P<event_slug>[-\w]+)/$', EventDetail.as_view(), name="event_detail"),
    url(r'^events/apply/(?P<requirement_id>[-\d]+)/$', ApplyForRequirement.as_view(), name="event_apply"),
]
