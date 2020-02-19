import math
import urllib
import urllib.parse as urlparse
from django import template
from django.template import Library
from django.template.base import token_kwargs

register = Library()

class PaginateNode(template.Node):
    def __init__(self,currentpage,pagesize,resultcount):
        self.currentpage = currentpage
        self.pagesize=pagesize
        self.resultcount = resultcount

    @staticmethod
    def base_paginate(requrl, pagesize, currentpage, resultcount):
        totalpages = math.ceil(float(resultcount)/pagesize)
        if currentpage < 3:
            start = 1
        else:
            start = currentpage - 2
        end = int(min(start + 4,totalpages))
        nextpage = min(currentpage+1,pagesize)
        prevpage = max(1,currentpage-1)
        urlparts = urlparse.urlsplit(requrl)
        query_dict = dict(urlparse.parse_qs(urlparts.query))
        query_dict = { k:','.join(v) for k,v in query_dict.items() if k!= 'alert_message'}
        query_dict['page'] = prevpage
        return totalpages, start, end, nextpage, urlparts, query_dict

    def render(self,context):
        currentpage = int(self.currentpage.resolve(context))
        pagesize = int(self.pagesize.resolve(context))
        resultcount = int(self.resultcount.resolve(context))
        request = context.get('request')
        requrl = request.build_absolute_uri()
        totalpages, start, end, nextpage, urlparts, query_dict = \
            PaginateNode.base_paginate(requrl, pagesize, currentpage, resultcount)
        if totalpages:
            if currentpage == start:
                tplstr = ''
            else:
                tplstr = '<li><a href="%s?%s">&laquo;</a></li>' % (urlparts.path,urllib.urlencode(query_dict),)
            for page in range(start,end+1):
                query_dict['page'] = page
                tplstr += '<li %s><a href="%s%s%s">%i</a></li>' % ('class="active"' if currentpage==page else '',urlparts.path,'?' if query_dict else '',urllib.urlencode(query_dict),page,)
            query_dict['page'] = nextpage
            if currentpage != totalpages:
                tplstr += '<li><a href="%s?%s">&raquo;</a></li>' % (urlparts.path,urllib.urlencode(query_dict),)
        else:
            tplstr = ""
        return tplstr


@register.tag(name='paginate')
def paginate(parser,token):
    bits = token.split_contents()
    remaining_bits = bits[1:]
    kwargs = token_kwargs(remaining_bits, parser, support_legacy=True)
    pagesize = kwargs.get('pagesize',10)
    currentpage = kwargs.get('currentpage',1)
    resultcount = kwargs.get('resultcount',None)
    if not resultcount:
        raise template.TemplateSyntaxError("'paginate' tag must have resultcount as one of its parameter")
    return PaginateNode(currentpage,pagesize,resultcount)
