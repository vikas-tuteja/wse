import django_filters
from models import UserDetail

class UserFilters(django_filters.FilterSet):
    username = django_filters.Filter(method = "get_username")

    class Meta:
        model = UserDetail 
        fields = ('username',) 

    def get_username(self, queryset, name, value):
        qs = queryset.filter(auth_user__username=value)
        return qs
