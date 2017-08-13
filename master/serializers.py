
from rest_framework import serializers
from models import Area, City

class AreaSerializer( serializers.ModelSerializer ):
    #city = serializers.ReadOnlyField(source='city.name')

    class Meta: 
        model = Area
        fields = ('id', 'name', 'slug')

class CitySerializer( serializers.ModelSerializer ):
    class Meta: 
        model = City 
        fields = ('id', 'name', 'slug')
