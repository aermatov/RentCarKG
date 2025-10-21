from django.contrib import admin
from . import models


@admin.register(models.CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(models.CarBody)
class CarBodyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(models.CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'mark']
    list_filter = ['mark']
    search_fields = ['name', 'mark__name']


@admin.register(models.FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(models.CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class CarImageInline(admin.TabularInline):
    model = models.CarImage
    extra = 1
    fields = ['image', 'order']


@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'mark', 'model', 'year', 'price_per_day',
        'transmission', 'is_available', 'created_at'
    ]
    list_filter = [
        'mark', 'model', 'body', 'fuel_type',
        'transmission', 'drive_type', 'is_available'
    ]
    search_fields = ['mark__name', 'model__name', 'color']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CarImageInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('mark', 'model', 'year', 'body', 'fuel_type')
        }),
        ('Технические характеристики', {
            'fields': ('horse_power', 'engine_volume', 'transmission',
                       'drive_type', 'seat', 'mileage')
        }),
        ('Внешний вид', {
            'fields': ('color', 'preview_img')
        }),
        ('Аренда', {
            'fields': ('price_per_day', 'is_available', 'description')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(models.CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'order']
    list_filter = ['car']


@admin.register(models.Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'car', 'rent_start', 'rent_end',
        'status', 'total_price', 'created_at'
    ]
    list_filter = ['status', 'rent_start', 'rent_end']
    search_fields = ['car__mark__name', 'car__model__name']
    readonly_fields = ['total_price', 'created_at']

    fieldsets = (
        ('Аренда', {
            'fields': ('car', 'rent_start', 'rent_end', 'status')
        }),
        ('Финансы', {
            'fields': ('total_price',)
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
