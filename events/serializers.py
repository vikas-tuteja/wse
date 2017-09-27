import datetime
from rest_framework import serializers
from collections import OrderedDict

from users.models import CandidateType
from users.choices import LANGUAGE_PROFICIENCY
from models import Event, Requirement, RequirementApplication

class ListEventSerializer( serializers.ModelSerializer ):
    client = serializers.CharField(read_only=True, source='client.auth_user.username')
    area = serializers.CharField(read_only=True, source='area.name')
    city = serializers.CharField(read_only=True, source='city.name')
    state = serializers.CharField(read_only=True, source='city.state.name')
    posted_by = serializers.CharField(read_only=True, source='event_posted_by.auth_user.username')
    candidate_info = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    contact_person_name = serializers.SerializerMethodField()


    class Meta:
        model = Event
        fields = ('id', 'client', 'name', 'slug', 'overview', 'venue', 'area', 'city', 'state', 'posted_by', 'contact_person_name', 'contact_person_number', 'candidate_info', 'schedule', 'briefing_datetime', 'short_description', 'is_applied')
    
    def get_contact_person_name(self, obj):
        return obj.contact_person_name or "-"

    def get_is_applied(self, obj):
        try:
            user = self.context['request']._request.user
            if not user:
                return False
            else:
                appl = RequirementApplication.objects.filter(
                    candidate = user,
                    requirement__in = list(obj.requirement_set.all())
                )
                if not appl:
                    return False
                else:
                    return appl[0].application_status
        except:
            return False


    def get_candidate_info(self, obj):
        candidates_required, paisa = {}, []
            
        for req in obj.requirement_set.all():
            candidates_required[req.gender] = candidates_required.get(req.gender, 0) + req.no_of_candidates
            paisa.append(req.daily_wage_per_candidate)
            
        return {
            'candidates_required' : candidates_required,
            'paisa': max(paisa or [0,])
        }


class ListRequirementSerializer( serializers.ModelSerializer ):
    candidate_type = serializers.CharField(read_only=True, source='candidate_type.name')
    event_slug = serializers.CharField(read_only=True, source='event.slug')
    communication_criteria = serializers.SerializerMethodField()

    class Meta:
        model = Requirement
        fields = ('id', 'event_slug', 'candidate_type', 'gender', 'no_of_candidates', 'no_of_days', 'daily_wage_per_candidate', 'dress_code', 'candidate_class', 'communication_criteria' )

    def get_communication_criteria(self, obj):
        return dict(LANGUAGE_PROFICIENCY).get(obj.communication_criteria)


class EventDetailSerializer( ListEventSerializer ):
    requirement_details = ListRequirementSerializer(many=True, source='requirement_set')
    schedule = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    is_valid = serializers.SerializerMethodField()
    candidate_info = serializers.SerializerMethodField()
    briefing_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_briefing_datetime(self, obj):
        if obj.briefing_datetime:
            return obj.briefing_datetime.strftime('%b %d, %Y')
        return None

    def get_candidate_info(self, obj):
        candidates_required, paisa = {}, []
            
        for req in obj.requirement_set.all():
            candidates_required[req.gender] = candidates_required.get(req.gender, 0) + req.no_of_candidates
            paisa.append(req.daily_wage_per_candidate)
            
        return {
            'candidates_required' : candidates_required,
            'paisa': max(paisa or [0,])
        }



    def get_is_valid(self, obj):
        sch  = obj.schedule()
        if sch and sch[1] > datetime.datetime.now().date():
            return True
        return False
            

    def get_schedule(self, obj):
        return obj.schedule()


    def get_details(self, obj):
        details_dict = OrderedDict([
            ('Eligibility', obj.eligibility),
            ('Selection & Screening', obj.selection_n_screening),
            ('Venue & Timing Details', obj.venue_n_timing),
            ('Payments', obj.payments),
            ('T & C', obj.t_n_c)
        ])

        return details_dict


class ApplyRequirementSerializer( serializers.ModelSerializer ):
    class Meta:
        model = RequirementApplication
        fields = '__all__'


class ProfileEventSerializer( ListEventSerializer ):
    req = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'client', 'name', 'slug', 'overview', 'venue', 'area', 'city', 'state', 'posted_by', 'contact_person_name', 'contact_person_number', 'candidate_info', 'schedule', 'briefing_datetime', 'short_description', 'req')


    def get_req(self, obj):
        req = []
        for x in obj.requirement_set.all():
            r = {
                'id':x.id,
                'type':x.candidate_type.name,
            }
            for each in x.requirementapplication_set.filter():
                r['application_status'] = each.application_status
                r['candidate'] = each.candidate.id
                r['payments'] = []
                for allocation in each.allocationstatus_set.all():
                    al = {
                        'allocation_status':allocation.allocation_status,
                        'paisa':x.daily_wage_per_candidate,
                    }
                    r['payments'].append(al)
            req.append(r)
        return req



class CandidateTypeSerializer( serializers.ModelSerializer ):
    class Meta:
        model = CandidateType
        fields = ('id', 'name', 'slug')

