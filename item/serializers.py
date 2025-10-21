from rest_framework import serializers
from . import models


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarMark
        fields = ['id', 'name']


class CarBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarBody
        fields = ['id', 'name']


class CarModelSerializer(serializers.ModelSerializer):
    mark_name = serializers.CharField(source='mark.name', read_only=True)

    class Meta:
        model = models.CarModel
        fields = ['id', 'name', 'mark', 'mark_name']


class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FuelType
        fields = ['id', 'name']


class CarColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarColor
        fields = ['id', 'name']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarImage
        fields = ['id', 'image', 'order']


class CarListSerializer(serializers.ModelSerializer):
    """списки (карточки)"""
    mark_name = serializers.CharField(source='mark.name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    body_name = serializers.CharField(source='body.name', read_only=True)
    fuel_type_name = serializers.CharField(source='fuel_type.name', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)

    class Meta:
        model = models.Car
        fields = [
            'id', 'mark_name', 'model_name', 'year', 'price_per_day',
            'preview_img', 'body_name', 'seat', 'transmission',
            'fuel_type_name', 'color_name', 'is_available'
        ]


class CarDetailSerializer(serializers.ModelSerializer):
    """детали автомобиля"""
    mark = CarMarkSerializer(read_only=True)
    model = CarModelSerializer(read_only=True)
    body = CarBodySerializer(read_only=True)
    fuel_type = FuelTypeSerializer(read_only=True)
    color = CarColorSerializer(read_only=True)
    images = CarImageSerializer(many=True, read_only=True)

    mark_id = serializers.PrimaryKeyRelatedField(
        queryset=models.CarMark.objects.all(),
        source='mark',
        write_only=True
    )
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=models.CarModel.objects.all(),
        source='model',
        write_only=True
    )
    body_id = serializers.PrimaryKeyRelatedField(
        queryset=models.CarBody.objects.all(),
        source='body',
        write_only=True
    )
    fuel_type_id = serializers.PrimaryKeyRelatedField(
        queryset=models.FuelType.objects.all(),
        source='fuel_type',
        write_only=True
    )
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=models.CarColor.objects.all(),
        source='color',
        write_only=True
    )

    class Meta:
        model = models.Car
        fields = [
            'id', 'mark', 'model', 'body', 'fuel_type', 'color',
            'year', 'horse_power', 'seat', 'mileage',
            'price_per_day', 'transmission', 'drive_type',
            'engine_volume', 'description',
            'preview_img', 'images', 'is_available',
            'created_at', 'updated_at',
            # Write-only поля
            'mark_id', 'model_id', 'body_id', 'fuel_type_id', 'color_id'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CarCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Car
        fields = [
            'id', 'mark', 'model', 'body', 'fuel_type', 'color',
            'year', 'horse_power', 'seat', 'mileage',
            'price_per_day', 'transmission', 'drive_type',
            'engine_volume', 'description',
            'preview_img', 'is_available'
        ]


class RentSerializer(serializers.ModelSerializer):
    car_info = CarListSerializer(source='car', read_only=True)

    class Meta:
        model = models.Rent
        fields = [
            'id', 'car', 'car_info', 'rent_start', 'rent_end',
            'status', 'total_price', 'created_at'
        ]
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        rent_start = data.get('rent_start')
        rent_end = data.get('rent_end')
        car = data.get('car')

        if rent_start and rent_end:
            if rent_end < rent_start:
                raise serializers.ValidationError(
                    "Дата окончания не может быть раньше даты начала"
                )

        if car and rent_start and rent_end:
            overlapping_rents = models.Rent.objects.filter(
                car=car,
                status__in=['pending', 'active'],
                rent_start__lte=rent_end,
                rent_end__gte=rent_start
            )

            if self.instance:
                overlapping_rents = overlapping_rents.exclude(id=self.instance.id)

            if overlapping_rents.exists():
                raise serializers.ValidationError(
                    "Автомобиль уже забронирован на эти даты"
                )

        return data


class RentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Rent
        fields = ['car', 'rent_start', 'rent_end']