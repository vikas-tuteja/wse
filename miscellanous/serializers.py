import json
from rest_framework import serializers
from models import Miscellaneous

class FaqSerializer( serializers.ModelSerializer ):
    faq = serializers.SerializerMethodField()
    class Meta:
        model = Miscellaneous
        fields = ('faq',)

    def get_faq(self, obj):
        return json.loads(obj.faq_content)

class AboutUsSerializer( serializers.ModelSerializer ):
    aboutus = serializers.SerializerMethodField()
    class Meta:
        model = Miscellaneous
        fields = ('aboutus',)

    def get_aboutus(self, obj):
        return json.loads(obj.aboutus_content)

class ContactUsSerializer( serializers.ModelSerializer ):
    contactus = serializers.SerializerMethodField()
    class Meta:
        model = Miscellaneous
        fields = ('contactus',)

    def get_contactus(self, obj):
        return json.loads(obj.contactus_content)
