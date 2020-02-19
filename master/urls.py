from django.conf.urls import url
from .views import AreaList

urlpatterns = [
    url(r'^arealisting/$', AreaList.as_view()),
]
