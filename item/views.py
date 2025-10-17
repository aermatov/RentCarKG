from rest_framework import generics
from . import models, serializers

class CarListAPIView(generics.ListAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarListSerializer
