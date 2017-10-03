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
from django.http import HttpResponse
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from master.management.commands.create_sitemap import sitemaps
from django.contrib.sitemaps.views import sitemap as dsitemap
from django.conf.urls import include
from views import Home
from master.sitemap import sitemap, sitemap_redirect

# url patterns here
urlpatterns = [
    url(r'^google7016c5c21c248bea.html', lambda r: HttpResponse("google-site-verification: google7016c5c21c248bea.html", content_type="text/plain")),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='text/xml')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^$', Home.as_view(), name="home"), 
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', django.views.static.serve,  {'document_root': settings.STATIC_ROOT }),
    url(r'^uploads/profile/(?P<path>.*)$', django.views.static.serve,  {'document_root': '%s/uploads/profile' % settings.BASE_DIR }),
    #url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$', dsitemap, {'sitemaps': sitemaps}, name="section_sitemap"),
    url(r'^sitemap_(?P<section>.+)$', sitemap_redirect, name="redirect_section"),
    url(r'^master/', include('master.urls')),
    url(r'^', include( 'events.urls' )),
    url(r'^', include('seo.urls')),
    url(r'^', include( 'users.urls' )),
    url(r'^', include( 'miscellanous.urls' )),
]
