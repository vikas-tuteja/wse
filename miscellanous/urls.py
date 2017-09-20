from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^faqs/$', Faqs.as_view(), name="faqs"),
    url(r'^clients/$', Clients.as_view(), name="clients"),
    url(r'^contact_us/$', ContactUs.as_view(), name="contact_us"),
    url(r'^about_us/$', AboutUs.as_view(), name="about_us"),

    url(r'^termsandconditions/$', TNC.as_view(), name="tnc"),
    url(r'^privacypolicy/$', PrivacyPolicy.as_view(), name="privacypolicy"),
    url(r'^article/tips-for-impeccable-events-staff-hiring/$', Articles.as_view(), name="articles"),
    url(r'^testimonials/$', Testimonials.as_view(), name="testimonials"),
]
