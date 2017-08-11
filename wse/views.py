from rest_framework import generics

from django.contrib.auth.models import User
from users.serializers import AuthUserSerializer

class Home( generics.ListAPIView ):
    serializer_class = AuthUserSerializer
    queryset = User.objects.none()
    template_name = "home/home.html"
