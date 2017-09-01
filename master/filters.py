import django_filters
from datetime import datetime

from models import Area
from events.models import Event

class AreaFilters(object):
    """
    filters from url patterns, not used as of now

    """
    def filter_queryset(self, request, queryset, view):
        if '/events/' in request.path:
            existing_events_area = Event.objects.filter(schedule__start_date__gte=datetime.now(), show_on_site=1).prefetch_related('area').values_list('area__slug', flat=True).distinct()
            qs = queryset.filter(slug__in=existing_events_area)
            return qs
        else:
            return queryset
