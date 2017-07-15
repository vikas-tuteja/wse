"""wse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import include

# url patterns here
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='shared/coming_soon2.html'), name="home"), 
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', django.views.static.serve,  {'document_root': settings.STATIC_ROOT }),
    url(r'^', include( 'events.urls' )),
    url(r'^', include('seo.urls')),
    url(r'^', include( 'users.urls' )),
    url(r'^master/', include('master.urls')),
]
