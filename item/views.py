from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from . import models, serializers, filters


class CarMarkListAPIView(generics.ListAPIView):
    queryset = models.CarMark.objects.all()
    serializer_class = serializers.CarMarkSerializer


class CarBodyListAPIView(generics.ListAPIView):
    queryset = models.CarBody.objects.all()
    serializer_class = serializers.CarBodySerializer


class CarModelListAPIView(generics.ListAPIView):
    queryset = models.CarModel.objects.all()
    serializer_class = serializers.CarModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mark']


class FuelTypeListAPIView(generics.ListAPIView):
    queryset = models.FuelType.objects.all()
    serializer_class = serializers.FuelTypeSerializer


class CarColorListAPIView(generics.ListAPIView):
    queryset = models.CarColor.objects.all()
    serializer_class = serializers.CarColorSerializer


class CarListAPIView(generics.ListAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = filters.CarFilter
    ordering_fields = ['price_per_day', 'year', 'mileage', 'created_at']
    ordering = ['-created_at']


class CarDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Car.objects.prefetch_related('images').select_related(
        'mark', 'model', 'body', 'fuel_type'
    )
    serializer_class = serializers.CarDetailSerializer


class CarCreateAPIView(generics.CreateAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarCreateUpdateSerializer


class CarUpdateAPIView(generics.UpdateAPIView):
    """Обновление автомобиля (PUT/PATCH)"""
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarCreateUpdateSerializer


class CarDeleteAPIView(generics.DestroyAPIView):
    """Удаление автомобиля"""
    queryset = models.Car.objects.all()


@api_view(['GET'])
def car_similar(request, pk):
    try:
        car = models.Car.objects.get(pk=pk)
    except models.Car.DoesNotExist:
        return Response(
            {'error': 'Автомобиль не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Ищем похожие по марке или близкой цене (±20%)
    price_min = car.price_per_day * 0.8
    price_max = car.price_per_day * 1.2

    similar_cars = models.Car.objects.filter(
        Q(mark=car.mark) | Q(price_per_day__range=(price_min, price_max))
    ).exclude(id=car.id).distinct()[:6]

    serializer = serializers.CarListSerializer(similar_cars, many=True)
    return Response(serializer.data)


class CarImageCreateAPIView(generics.CreateAPIView):
    queryset = models.CarImage.objects.all()
    serializer_class = serializers.CarImageSerializer


class CarImageDeleteAPIView(generics.DestroyAPIView):
    queryset = models.CarImage.objects.all()


class RentListAPIView(generics.ListAPIView):
    queryset = models.Rent.objects.select_related('car').all()
    serializer_class = serializers.RentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = filters.RentFilter
    ordering_fields = ['rent_start', 'rent_end', 'created_at']
    ordering = ['-created_at']


class RentDetailAPIView(generics.RetrieveAPIView):
    queryset = models.Rent.objects.select_related('car').all()
    serializer_class = serializers.RentSerializer


class RentCreateAPIView(generics.CreateAPIView):
    queryset = models.Rent.objects.all()
    serializer_class = serializers.RentSerializer


class RentUpdateAPIView(generics.UpdateAPIView):
    queryset = models.Rent.objects.all()
    serializer_class = serializers.RentSerializer


class RentDeleteAPIView(generics.DestroyAPIView):
    queryset = models.Rent.objects.all()


@api_view(['GET'])
def rent_check_availability(request):
    car_id = request.query_params.get('car_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not all([car_id, start_date, end_date]):
        return Response(
            {'error': 'Необходимы параметры: car_id, start_date, end_date'},
            status=status.HTTP_400_BAD_REQUEST
        )

    overlapping = models.Rent.objects.filter(
        car_id=car_id,
        status__in=['pending', 'active'],
        rent_start__lte=end_date,
        rent_end__gte=start_date
    ).exists()

    return Response({'available': not overlapping})
