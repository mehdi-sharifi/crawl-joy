from rest_framework import serializers
from .models import Person, CarAd

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class PersonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'last_name', 'email']

class CarAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAd
        fields = '__all__'
        
class NotificationSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100)
    url = serializers.CharField()
    title = serializers.CharField(max_length=100)
    year = serializers.CharField(max_length=100)
    mileage = serializers.CharField()
    price = serializers.CharField()
    
class CrawlerSerializer(serializers.Serializer):
    code = serializers.CharField()
    url = serializers.URLField()
    title = serializers.CharField()
    price = serializers.IntegerField()
    year = serializers.IntegerField()
    mileage = serializers.IntegerField()
    color = serializers.CharField()
    body_status = serializers.CharField()
    modified_date = serializers.DateTimeField()