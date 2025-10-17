from rest_framework import serializers
from . import models

class CarListSerializer(serializers.ModelSerializer):
    mark_name = serializers.CharField(source='mark.name')
    model_name = serializers.CharField(source='model.name')
    year = serializers.CharField()
    horse_power = serializers.CharField()
    seat = serializers.CharField()
    body = serializers.CharField()
    mileage = serializers.CharField()
    preview_img = serializers.ImageField

    class Meta:
        model = models.Car
        fields = ['mark_name', 'model_name', 'year', 'horse_power', 'seat', 'body', 'mileage', 'preview_img']
