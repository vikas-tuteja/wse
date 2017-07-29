from rest_framework import serializers

from django.contrib.auth.models import User
from models import UserDetail, CandidateAttribute


class AuthUserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = ('username', 'email', )


class UserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = UserDetail
        fields = '__all__'


class UserMeterSerializer( serializers.ModelSerializer ):
    candidate = serializers.SerializerMethodField()
    
    class Meta:
        model = UserDetail
        fields = ('auth_user', 'type', 'mobile', 'whatsapp_number', 'address', 'image', 'area', 'city', 'state', 'blacklist_flag', 'candidate')

    def get_candidate(self, obj):
        candidate_attribute = obj.candidateattribute_set.all()
        candidate_fields = ('language_proficiency', 'looks', 'open_to_which_kind_of_job', 'pay_scale', 'comfortable_travelling_outdoor', 'comfortable_for_liquor_promotion', 'comfortable_working_at_odd_timings')

        candidate_data = {}
        if candidate_attribute:
            for field in candidate_fields:
                candidate_data[field] = eval("candidate_attribute[0].%s" % field)
            return candidate_data
        return {}
