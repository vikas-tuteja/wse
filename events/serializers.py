from rest_framework import serializers

from models import Event, Requirement, RequirementApplication

class ListEventSerializer( serializers.ModelSerializer ):
    client = serializers.CharField(read_only=True, source='client.auth_user.username')
    area = serializers.CharField(read_only=True, source='area.name')
    city = serializers.CharField(read_only=True, source='city.name')
    state = serializers.CharField(read_only=True, source='city.state.name')
    posted_by = serializers.CharField(read_only=True, source='event_posted_by.auth_user.username')
    candidate_info = serializers.SerializerMethodField()
    req = serializers.SerializerMethodField()
    #userprofile_status = serializers.SerializerMethodField()


    class Meta:
        model = Event
        fields = ('id', 'client', 'name', 'slug', 'overview', 'venue', 'area', 'city', 'state', 'posted_by', 'contact_person_name', 'contact_person_number', 'candidate_info', 'schedule', 'req', 'briefing_datetime', 'short_description')

    def get_candidate_info(self, obj):
        candidates_required, paisa = {}, []
            
        for req in obj.requirement_set.all():
            candidates_required[req.gender] = candidates_required.get(req.gender, 0) + req.no_of_candidates
            paisa.append(req.daily_wage_per_candidate)
            
        return {
            'candidates_required' : candidates_required,
            'paisa': max(paisa)
        }

    def get_req(self, obj):
        req = []
        #import pdb; pdb.set_trace()
        for x in obj.requirement_set.all():
            r = {
                'id':x.id,
                'type':x.candidate_type.name,
            }
            for each in x.requirementapplication_set.filter():
                r['application_status'] = each.application_status
                r['candidate'] = each.candidate.id
                r['auth_id'] = each.candidate.auth_user.id
            req.append(r)
        return req


class ListRequirementSerializer( serializers.ModelSerializer ):
    candidate_type = serializers.CharField(read_only=True, source='candidate_type.name')
    event_slug = serializers.CharField(read_only=True, source='event.slug')

    class Meta:
        model = Requirement
        fields = ('id', 'event_slug', 'candidate_type', 'gender', 'no_of_candidates', 'no_of_days', 'daily_wage_per_candidate', 'dress_code', 'candidate_class', 'communication_criteria' )


class EventDetailSerializer( ListEventSerializer ):
    requirement_details = ListRequirementSerializer(many=True, source='requirement_set')

    class Meta:
        model = Event
        fields = '__all__'


class ApplyRequirementSerializer( serializers.ModelSerializer ):
    class Meta:
        model = RequirementApplication
        fields = '__all__'
