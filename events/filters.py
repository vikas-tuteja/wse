import django_filters

from models import Event

class EventFilters(django_filters.FilterSet):
    city = django_filters.CharFilter(name="city__slug")
    area = django_filters.CharFilter(name="area__slug")
    venue = django_filters.Filter(method="get_venue")

    class Meta:
        model = Event
        fields = ('city', 'area', 'venue') 

    def get_venue(self, queryset, name, value):
        qs = queryset.filter(venue__icontains=value)
        return qs

