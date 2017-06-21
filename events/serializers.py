from rest_framework import serializers

from models import Event

class ListEventSerializer(serializers.ModelSerializer):
    client = serializers.CharField(read_only=True, source='client.auth_user.username')
    area = serializers.CharField(read_only=True, source='area.name')
    city = serializers.CharField(read_only=True, source='city.name')
    state = serializers.CharField(read_only=True, source='city.state.name')
    posted_by = serializers.CharField(read_only=True, source='event_posted_by.auth_user.username')


    class Meta:
        model = Event
        fields = ('id', 'client', 'name', 'description', 'venue', 'area', 'city', 'state', 'posted_by', 'event_start_datetime', 'event_end_datetime', 'notes', 'contact_person_name', 'contact_person_number', 'total_payment' )
