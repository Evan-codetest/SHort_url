from rest_framework import serializers
from .models import Shorturl

class Urlserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shorturl
        fields = ('id','short_url','original_url','create_date')