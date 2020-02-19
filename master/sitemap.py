import os
import stat
import random
import http.client as httplib
import datetime
import urllib.parse as urlparse
from django.template import loader
from django.utils.http import http_date
from django.utils.encoding import smart_str
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from wse.settings import ROOT_BASE_URL
from events.models import Event
from django.conf import settings
XML_ROOT = settings.XML_ROOT


class SuperSitemap(Sitemap):
    Sitemap.limit = 35000
    success_count = 0
    write_file = None


    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def getStatus(self, ourl):
        return True
        if ourl:
            ourl = ourl.encode('ascii','ignore')
        else:
            ourl = str(ourl)
        try:
            url = urlparse(ourl)
            conn = httplib.HTTPConnection(url.netloc)
            conn.request("HEAD", url.path)
            res = conn.getresponse()
            if str(res.status) in ['404','500','302']:
                if SuperSitemap.write_file:
                    SuperSitemap.write_file.write(str(ourl)+','+str(res.status)+'\n')
                return False
            else:
                return True
        except:
            if SuperSitemap.write_file:
                SuperSitemap.write_file.write('Error in Pinging Url ,'+ ourl+'\n')
            return False

    def get_urls(self, page=1, count=-1,site=ROOT_BASE_URL):
        get_status = False
        inc_count = 0
        success_count = 0
        urls = []
        for item in self.paginator.page(page).object_list:
            url_list = self.__get('location', item)
            for each_url in url_list:
                loc = "http://%s%s" % (site, each_url)
                priority = self.__get('priority', item, None)
                url_info = {
                    'location':   loc,
                    'lastmod':    self.__get('lastmod', item, None),
                    #'changefreq': self.__get('changefreq', item, None),
                    'priority':   str(priority is not None and priority or '')
                }
                if (inc_count < count and random.random() < 0.3) or count == -1:
                    get_status = self.getStatus(loc)
                    inc_count += 1
                    if get_status:
                        urls.append(url_info)
                elif count == -2:
                    urls.append(url_info)
                else:
                    urls.append(url_info)
                success_count += 1
        return urls, success_count

    def lastmod(self, obj):
        return datetime.datetime.today()

    #def changefreq(self, obj):
    #    return random.choice(["hourly", "always"])

    def priority(self, obj):
        return random.choice([0.9, 1.0])

    def location(self, obj):
        return [obj]

def sitemap(request, sitemaps, section=None, template_name='custom_sitemap.xml'):
    current_site = request.get_host()
    urls = []
    os.chdir(XML_ROOT)
    if getattr(request,'subdomain',None) == 'm':
        os.chdir(XML_ROOT+'mobile/')
    for files in os.listdir("."):
        if files.endswith(".xml"):
            url_info = {
                'location':   'http://' + current_site + '/' + files,
                'lastmod':    datetime.datetime.today(),
                #'changefreq': random.choice(["hourly", "always"]),
                }
            urls.append(url_info)
    xml = smart_str(loader.render_to_string(template_name, {'urlset': urls}))
    return HttpResponse(xml, content_type='application/xml')



def sitemap_redirect(request, section=None):
    path = settings.XML_ROOT
    mobile = getattr(request,'subdomain',None) == 'm'
    if mobile and re.search(r'[a-z]\.xml$',section):
        path = settings.XML_ROOT + 'mobile/'
    elif mobile:
        path = settings.XML_ROOT + 'mobile/sitemap/'
    fullpath = (path + 'sitemap_' + section).replace('\\', '/')
    try:
        statobj = os.stat(fullpath)
    except:
        return HttpResponseRedirect(reverse('homepage'))
    #mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    contents = open(fullpath, 'rb').read()
    response = HttpResponse(contents, content_type='application/xml')
    response["Last-Modified"] = http_date(statobj[stat.ST_MTIME])
    if fullpath.endswith('.gz'):
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(fullpath)
    response["Content-Length"] = len(contents)
    return response



class EventDetailsSitemap( SuperSitemap ):
    """
    URL's generator for Event Detail Page
    
    Returns: list of all existing event detail page and
             only those tabs where start date is greater than now and show on site = 1

    """

    @classmethod
    def items(self):
        # fetch even slugs where show on site = 1 and start date > now
        event_details = Event.objects.filter(show_on_site=1, schedule__start_date__gte=datetime.datetime.now()).values_list('id', 'slug').distinct()

        # for each event
        event_detail_urls = []
        for event in event_details:
            # create detail url and append it to the event detail list
            event_detail_urls.append(
                reverse("event_detail", kwargs={
                    'event_slug': event[1],
                    'event_id': event[0]
                })
            )

        return event_detail_urls


class EventListingSitemap(SuperSitemap):
    @classmethod
    def items(self):
        listing_url = set(['/events/',])
        existing_events = Event.objects.filter(show_on_site=1,schedule__start_date__gte=datetime.datetime.now()).prefetch_related('area', 'city').values_list('area__slug', 'city__slug').distinct()

        for area, city in existing_events:
            # add area url
            listing_url.add(
                reverse("event_listing_area", kwargs={
                    'area_slug': area
                })
            )

            # add city url
            listing_url.add(
                reverse("event_listing_city", kwargs={
                    'city_slug': city
                })
            )

        return list(listing_url)
    

class ListingTypeSitemap(SuperSitemap):
    @classmethod
    def items(self):
        listing_url = ['/faqs/', '/contact_us/', '/about_us/', '/post-events/', '/article/tips-for-impeccable-events-staff-hiring/']
        return listing_url
    
