import django_filters

from models import Event

class EventFilters(django_filters.FilterSet):
    city = django_filters.CharFilter(name="city__slug")
    area = django_filters.CharFilter(name="area__slug")
    venue = django_filters.Filter(method="get_venue")
    name = django_filters.Filter(method="search_events")
    sort = django_filters.Filter(method="sort_data")
    user = django_filters.Filter(method="user_history")

    class Meta:
        model = Event
        fields = ('city', 'area', 'venue')

    def get_venue(self, queryset, name, value):
        qs = queryset.filter(venue__icontains=value)
        return qs

    def search_events(self, queryset, name, value):
        qs = queryset.filter(name__icontains=value)
        return qs

    def sort_data(self, queryset, name, value):
        value = value.replace('date', 'schedule__start_date')
        qs = queryset.order_by(value)
        return qs

    def user_history(self, queryset, name, value):
        qs = queryset.filter(requirement__requirementapplication__candidate__auth_user__email=value)
        return qs
