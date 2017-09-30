import django_filters
from datetime import datetime

from models import Area
from events.models import Event

class AreaFilters(object):
    """
    filters from url patterns, not used as of now

    """
    def filter_queryset(self, request, queryset, view):
        qs = queryset
        city_filter = request.GET.get('city')
        if city_filter:
            qs = qs.filter(city__slug=city_filter)

        if '/events/' in request.path or '/events-in-' in request.path:
            existing_events_area = Event.objects.filter(schedule__start_date__gte=datetime.now(), show_on_site=1).prefetch_related('area').values_list('area__slug', flat=True).distinct()
            qs = qs.filter(slug__in=existing_events_area)
            return qs
        else:
            return qs


class AreaqpFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(name="city__slug")

    class Meta:
        model = Area
        fields = ('city',)
