from django.contrib import admin
from django.utils.html import format_html
from .models import CarMark, CarModel, CarBody, FuelType, Car, CarImage, Rent


@admin.register(CarMark)
class CarMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(CarBody)
class CarBodyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(FuelType)
class FuelTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1  # сколько пустых строк для загрузки отображать
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="70" style="object-fit:cover; border-radius:4px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Превью"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'mark', 'model', 'year', 'horse_power', 'seat', 'body', 'mileage', 'preview_thumbnail')
    list_filter = ('mark', 'body', 'year')
    search_fields = ('mark__name', 'model__name')
    inlines = [CarImageInline]

    def preview_thumbnail(self, obj):
        if obj.preview_img:
            return format_html('<img src="{}" width="80" height="60" style="object-fit:cover; border-radius:4px;" />', obj.preview_img.url)
        return "-"
    preview_thumbnail.short_description = "Превью"


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'rent_start', 'rent_end', 'duration_days')
    list_filter = ('rent_start', 'rent_end', 'car__mark')
    search_fields = ('car__mark__name', 'car__model__name')

    def duration_days(self, obj):
        if obj.rent_start and obj.rent_end:
            return (obj.rent_end - obj.rent_start).days
        return "-"
    duration_days.short_description = "Длительность (дн.)"