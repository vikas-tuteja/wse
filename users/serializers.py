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


class CandidateSerializer( UserSerializer ):
    class Meta:
        model = CandidateAttribute
        fields = '__all__'
