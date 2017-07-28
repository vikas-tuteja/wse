from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^faqs/$', Faqs.as_view(), name="faqs"),
    url(r'^articles/$', Articles.as_view(), name="articles"),
    url(r'^clients/$', Clients.as_view(), name="clients"),
    url(r'^testimonials/$', Testimonials.as_view(), name="testimonials"),
    url(r'^contact_us/$', ContactUs.as_view(), name="contact_us"),
    url(r'^about_us/$', AboutUs.as_view(), name="about_us"),
]
