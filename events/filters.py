import django_filters

from models import Event


class EventFilterBackend(object):
    """
    filters from url patterns, not used as of now

    """
    def filter_queryset(self, request, queryset, view):
        area_slug = view.kwargs.get('area_slug')
        if area_slug:
            queryset = queryset.filter(area__slug=area_slug)

        userrole = view.kwargs.get('userrole', 'candidate')
        if userrole == 'candidate':
            try:
                value = request.query_params.get('userprofile')
                if not value:
                    value = view.kwargs.get('userprofile')
                int(value)
            except:
                return queryset
      
            qs = set()
            for eachqs in queryset:
                for req in eachqs.requirement_set.all():
                    for app in req.requirementapplication_set.filter(candidate__id=value):
                        #for allocation in app.allocationstatus_set.filter():
                        qs.add(eachqs)
        
            return list(qs)

        elif userrole == 'client':
            return queryset.filter(client=request.user)


class EventFilters(django_filters.FilterSet):
    """
    filters from kwargs

    """
    city = django_filters.CharFilter(name="city__slug")
    area = django_filters.Filter(method="get_area")
    venue = django_filters.Filter(method="get_venue")
    name = django_filters.Filter(method="search_events")
    sort = django_filters.Filter(method="sort_data")
    user = django_filters.Filter(method="user_history")
    gender = django_filters.Filter(method="get_gender")
    requirement = django_filters.Filter(method="get_requirement_type")
    duration = django_filters.Filter(method="get_duration")
    #userprofile = django_filters.Filter(method="get_userprofile")


    class Meta:
        model = Event
        fields = ('venue', 'city', 'area')


    def get_area(self, queryset, name, value):
        qs = queryset.filter(area__slug__in=value.split(','))
        return qs

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

    def get_gender(self, queryset, name, value):
        qs = queryset.filter(requirement__gender=value)
        return qs

    def get_requirement_type(self, queryset, name, value):
        qs = queryset.filter(requirement__candidate_type__slug__in=value.split(','))
        return qs

    def get_duration(self, queryset, name, value):
        # TODO add days filter
        if value == '1':
            qs = [ x for x in queryset.all() if x.schedule()[2] == 1 ]
        elif value == '7':
            qs = [ x for x in queryset.all() if x.schedule()[2] <= 7 ]
        elif value == '8':
            qs = [ x for x in queryset.all() if x.schedule()[2] >= 8 ]
        elif value == '2':
            # only weeknd events
            qs = []
            for obj in queryset.all():
                weekend = True
                for each_date in obj.schedule_set.all():
                    if each_date.start_date.isoweekday() not in (6,7):
                        weekend = False
                        break
                
                if weekend:
                    qs.append(obj)

        return qs

    """def get_userprofile(self, queryset, name, value):
        qs = []
        try:
            int(value)
        except:
            return qs
  
        for eachqs in queryset:
            for req in eachqs.requirement_set.all():
                for app in req.requirementapplication_set.filter(candidate__id=value):
                    for allocation in app.allocationstatus_set.filter(allocation_status='shortlisted'):
                        qs.append(eachqs)
    
        return qs"""
