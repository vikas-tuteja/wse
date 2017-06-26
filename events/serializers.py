from rest_framework import serializers

from models import Event, Requirement

class ListEventSerializer( serializers.ModelSerializer ):
    client = serializers.CharField(read_only=True, source='client.auth_user.username')
    area = serializers.CharField(read_only=True, source='area.name')
    city = serializers.CharField(read_only=True, source='city.name')
    state = serializers.CharField(read_only=True, source='city.state.name')
    posted_by = serializers.CharField(read_only=True, source='event_posted_by.auth_user.username')
    candidate_info = serializers.SerializerMethodField()


    class Meta:
        model = Event
        fields = ('id', 'client', 'name', 'slug', 'overview', 'venue', 'area', 'city', 'state', 'posted_by', 'notes', 'contact_person_name', 'contact_person_number', 'candidate_info' )

    def get_candidate_info(self, obj):
        candidates_required = 0
        for req in obj.requirement_set.all():
            candidates_required += req.no_of_candidates
            
        return {
            'candidates_required' : candidates_required,
            'days' : req.no_of_days,
        }


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
