from rest_framework import serializers

from django.contrib.auth.models import User
from models import UserDetail, CandidateAttribute
from utility.fields import UserDetailFields, ClientAttributeFields, CandidateAttributeFields
from utility.utils import null_to_empty, substring

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
        try:
            return substring("/%s"% getattr(obj.image, 'url', None), '/uploads')
        except:
            return None


class UserMeterSerializer( serializers.ModelSerializer ):
    whatsapp_number = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    auth_user = serializers.SerializerMethodField()
    candidate = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    area = serializers.CharField(read_only=True, source='area.slug')
    city = serializers.CharField(read_only=True, source='city.slug')
    highest_qualification = serializers.CharField(read_only=True, source='highest_qualification.slug')
    type = serializers.CharField(read_only=True, source='type.slug')
    
    class Meta:
        model = UserDetail
        fields = UserDetailFields

    @null_to_empty
    def get_image(self, obj):
        try:
            return substring("/%s"% getattr(obj.image, 'url', None), '/uploads')
        except:
            None

    @null_to_empty
    def get_address(self, obj):
        return obj.address

    @null_to_empty
    def get_whatsapp_number(self, obj):
        return obj.whatsapp_number

    def get_auth_user(self, obj):
        return {
            'first_name': obj.auth_user.first_name,
            'last_name': obj.auth_user.last_name,
        }

    def get_candidate(self, obj):
        candidate_data = {}
        if obj.type.slug == 'candidate':
            candidate_attribute = obj.candidateattribute_set.all()
            candidate_fields = CandidateAttributeFields

            if candidate_attribute:
                for field in candidate_fields:
                    candidate_data[field] = eval("candidate_attribute[0].%s" % field) or ""
            else:
                [ candidate_data.update({field:""}) for field in candidate_fields ]

        return candidate_data


    def get_client(self, obj):
        client_data = {}
        if obj.type.slug == 'client':
            client_attribute = obj.clientattribute_set.all()
            client_fields = ClientAttributeFields

            if client_attribute:
                for field in client_fields:
                    client_data[field] = eval("client_attribute[0].%s" % field) or ""
            else:
                [ client_data.update({field:""}) for field in client_fields ]

        return client_data
