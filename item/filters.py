from django_filters import rest_framework as filters
from django.db.models import Q
from . import models
from .choices import TRANSMISSION_CHOICES, DRIVE_TYPE_CHOICES, RENT_STATUS_CHOICES


class CarFilter(filters.FilterSet):
    mark = filters.NumberFilter(field_name='mark__id')
    model = filters.NumberFilter(field_name='model__id')
    body = filters.NumberFilter(field_name='body__id')
    fuel_type = filters.NumberFilter(field_name='fuel_type__id')
    color = filters.NumberFilter(field_name='color__id')
    transmission = filters.ChoiceFilter(choices=TRANSMISSION_CHOICES)
    drive_type = filters.ChoiceFilter(choices=DRIVE_TYPE_CHOICES)

    year_min = filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = filters.NumberFilter(field_name='year', lookup_expr='lte')

    price_min = filters.NumberFilter(field_name='price_per_day', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price_per_day', lookup_expr='lte')

    mileage_min = filters.NumberFilter(field_name='mileage', lookup_expr='gte')
    mileage_max = filters.NumberFilter(field_name='mileage', lookup_expr='lte')

    horse_power_min = filters.NumberFilter(field_name='horse_power', lookup_expr='gte')
    horse_power_max = filters.NumberFilter(field_name='horse_power', lookup_expr='lte')

    seat = filters.NumberFilter(field_name='seat')

    search = filters.CharFilter(method='search_filter')

    is_available = filters.BooleanFilter()

    class Meta:
        model = models.Car
        fields = [
            'mark', 'model', 'body', 'fuel_type', 'transmission',
            'drive_type', 'year_min', 'year_max', 'price_min',
            'price_max', 'mileage_min', 'mileage_max',
            'horse_power_min', 'horse_power_max', 'seat',
            'is_available'
        ]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(mark__name__icontains=value) |
            models.Q(model__name__icontains=value) |
            models.Q(color__icontains=value)
        )


class RentFilter(filters.FilterSet):
    car = filters.NumberFilter(field_name='car__id')
    status = filters.ChoiceFilter(choices=RENT_STATUS_CHOICES)
    rent_start = filters.DateFilter(field_name='rent_start', lookup_expr='gte')
    rent_end = filters.DateFilter(field_name='rent_end', lookup_expr='lte')

    class Meta:
        model = models.Rent
        fields = ['car', 'status', 'rent_start', 'rent_end']
