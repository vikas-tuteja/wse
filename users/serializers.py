from rest_framework import serializers

from django.contrib.auth.models import User
from models import UserDetail


class AuthUserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = ('username', 'email', )


class UserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = UserDetail
        fields = ('auth_user__username', 'authuser__email', 'mobile')
