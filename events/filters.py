import django_filters

from models import Event

class EventFilters(django_filters.FilterSet):
    city = django_filters.CharFilter(name="city__slug")
    area = django_filters.CharFilter(name="area__slug")
    venue = django_filters.Filter(method="get_venue")
    event_start = django_filters.DateFromToRangeFilter(name="event_start_datetime", lookup_expr="gte")
    event_end = django_filters.DateFromToRangeFilter(name="event_end_datetime", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ('city', 'area', 'venue', 'event_start', 'event_end')

    def get_venue(self, queryset, name, value):
        qs = queryset.filter(venue__icontains=value)
        return qs

