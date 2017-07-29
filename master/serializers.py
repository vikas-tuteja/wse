
from rest_framework import serializers
from models import Area

class AreaSerializer( serializers.ModelSerializer ):
    #city = serializers.ReadOnlyField(source='city.name')

    class Meta: 
        model = Area
        fields = ('id', 'name', 'slug')
