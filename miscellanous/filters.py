import django_filters

from miscellanous.models import Article

class ArticleFilters(object):
    def filter_queryset(self, request, queryset, view):
        slug = view.kwargs.get('slug')
        if slug:
            qs = queryset.filter(slug=slug)
            return qs

        return queryset
