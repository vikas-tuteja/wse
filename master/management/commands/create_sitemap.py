import os
import sys
import datetime
import traceback
from django.template import loader
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.core.management.base import BaseCommand

from wse.settings import BASE_DIR, ROOT_BASE_URL
from master.sitemap import SuperSitemap, EventDetailsSitemap, ListingTypeSitemap 
parent_xml_path = os.path.join(BASE_DIR, 'sitemap_xml/').replace('\\', '/')

sitemaps = {
    "event_details": EventDetailsSitemap,
    "listing": ListingTypeSitemap 
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        print "=/= " * 20, "\nSitemap creation started @ %s" %(datetime.datetime.now())
        count = -1
        if args:
            count = int(args[0]) if args[0].isdigit() else -1
        current_site = ROOT_BASE_URL
        root_url_path = 'http://%s/' % current_site
        sites = []
        today_date = datetime.date.today()
        try:
            global sitemaps
            for section, site in sitemaps.items():
                parent_xml_file = parent_xml_path + 'sitemap_' + section + '.xml'
                fd_parent = open(parent_xml_file, 'w')
                fd_parent.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                fd_parent.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

                fd_parent.write('<sitemap>\n')
                fd_parent.write('<loc>' + root_url_path + 'sitemap_' + section + '-1.xml.gz</loc>\n')
                fd_parent.write('<lastmod>' + today_date.strftime("%Y-%m-%d") + '</lastmod>\n')
                fd_parent.write('</sitemap>\n')
                if callable(site):
                    pages = site().paginator.num_pages
                else:
                    pages = site.paginator.num_pages
                sitemap_url = reverse('section_sitemap', kwargs={'section': section})
                sites.append('%s%s' % (current_site, sitemap_url))
                if pages > 1:
                    for page in range(2, pages + 1):
                        sites.append('%s%s?p=%s' % (current_site, sitemap_url, page))
                        fd_parent.write('<sitemap>\n')
                        fd_parent.write('<loc>' + root_url_path + 'sitemap_' + section + '-' + str(page) + '.xml.gz</loc>\n')
                        fd_parent.write('<lastmod>' + today_date.strftime("%Y-%m-%d") + '</lastmod>\n')
                        fd_parent.write('</sitemap>\n')

                fd_parent.write('</sitemapindex>\n')
                fd_parent.close()

            success_count = 0;
            SuperSitemap.write_file = open(BASE_DIR+'/uploads/sitemap_log.txt','w')
            for each_site in sites:
                url_name = each_site.split('/')[1]
                if url_name.find('?') > 0:
                    section = url_name[url_name.find('-') + 1:url_name.find('.')]
                    page = int(url_name[url_name.find('=') + 1:])
                else:
                    section = url_name[url_name.find('-') + 1:url_name.find('.')]
                    page = 1
                file_name = 'sitemap_' + section + '-' + str(page) + '.xml'
                xml_file_path = parent_xml_path + file_name
                maps, urls = [], []
                maps.append(sitemaps[section])
                for site in maps:
                    if callable(site):
                        urls, success_count = site().get_urls(page,count)
                    else:
                        urls, success_count = site.get_urls(page,count)
                response = smart_str(loader.render_to_string('custom_sitemap.xml', {'urlset': urls}))

                fd = open(xml_file_path, 'w')
                fd.write(response)
                fd.close()
                os.system(str('gzip -f ' + xml_file_path))

                if SuperSitemap.write_file:
                    SuperSitemap.write_file.write('XML File : %s , Success Count : %s\n' %(os.path.basename(xml_file_path), success_count))

            if not SuperSitemap.write_file.closed:
                    SuperSitemap.write_file.close()
        except Exception, e:
            error_stream = traceback.format_exc()
            sys.stdout.write(error_stream)
            sys.stdout.write('\nExiting with error\n'+'*'*30+'\n')
            sys.exit()

        sys.stdout.write('Successfully created the xml files\n\n')

