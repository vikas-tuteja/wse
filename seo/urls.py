from django.conf.urls import url
from .views import get_named_url_list

urlpatterns = [
        url( r'^seo/get_named_url_list/$', get_named_url_list, name = 'get_named_url_list' ),
    ]
