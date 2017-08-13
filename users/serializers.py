from rest_framework import serializers

from django.contrib.auth.models import User
from models import UserDetail, CandidateAttribute
from utility.fields import UserDetailFields, ClientAttributeFields, CandidateAttributeFields

class AuthUserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = ('username', 'password')


class AuthUserSer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class UserSerializer( serializers.ModelSerializer ):
    auth_id = serializers.CharField(read_only=True, source='auth_user.id')
    username = serializers.CharField(read_only=True, source='auth_user.username')
    email = serializers.CharField(read_only=True, source='auth_user.email')
    name = serializers.CharField(read_only=True, source='auth_user.first_name')
    image = serializers.SerializerMethodField()

    class Meta:
        model = UserDetail
        fields = ('auth_id', 'username','email','mobile', 'image', 'name')

    def get_image(self, obj):
        return "/%s"% getattr(obj, 'image.url', None)


class UserMeterSerializer( serializers.ModelSerializer ):
    candidate = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    type = serializers.CharField(read_only=True, source='type.slug')
    
    class Meta:
        model = UserDetail
        fields = UserDetailFields


    def get_candidate(self, obj):
        candidate_data = {}
        if obj.type.slug == 'candidate':
            candidate_attribute = obj.candidateattribute_set.all()
            candidate_fields = CandidateAttributeFields

            if candidate_attribute:
                for field in candidate_fields:
                    candidate_data[field] = eval("candidate_attribute[0].%s" % field)
            else:
                [ candidate_data.update({field:None}) for field in candidate_fields ]

        return candidate_data


    def get_client(self, obj):
        client_data = {}
        if obj.type.slug == 'client':
            client_attribute = obj.clientattribute_set.all()
            client_fields = ClientAttributeFields

            if client_attribute:
                for field in client_fields:
                    client_data[field] = eval("client_attribute[0].%s" % field)
            else:
                [ client_data.update({field:None}) for field in client_fields ]

        return client_data
