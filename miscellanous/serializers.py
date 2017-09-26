import json
from rest_framework import serializers
from models import Miscellaneous, Testimonial, Article
from users.serializers import AuthUserSer

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
        return obj.contactus_content


class TestimonialsSerializer( serializers.ModelSerializer ):
    author = AuthUserSer(source='user')
    class Meta:
        model = Testimonial
        fields = ('author', 'title', 'content')


class ArticleSerializer( serializers.ModelSerializer ):
    author = AuthUserSer(source='user')

    class Meta:
        model = Article
        fields = ('author', 'title', 'content', 'slug')

    def get_slug(self, obj):
        return slugify(obj.title)

class TNCSerializer( serializers.ModelSerializer ):
    tnc = serializers.SerializerMethodField()
    class Meta:
        model = Miscellaneous
        fields = ('tnc',)

    def get_tnc(self,obj):
        return obj.tnc

class PPSerializer( serializers.ModelSerializer ):
    privacypolicy = serializers.SerializerMethodField()
    class Meta:
        model = Miscellaneous
        fields = ('privacypolicy',)

    def get_privacypolicy(self,obj):
        return obj.privacypolicy
