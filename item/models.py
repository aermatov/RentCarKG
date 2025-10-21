from django.db import models
from .choices import (year_choices, SEAT_CHOICES, horse_power_choice, TRANSMISSION_CHOICES, DRIVE_TYPE_CHOICES,
                      RENT_STATUS_CHOICES)


class CarMark(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'
        ordering = ['-id']

    def __str__(self):
        return self.name


class CarBody(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)

    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузова'
        ordering = ['-id']

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    mark = models.ForeignKey(CarMark, on_delete=models.CASCADE, related_name='models', verbose_name='Марка')

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        ordering = ['-id']

    def __str__(self):
        return f"{self.mark.name} {self.name}"


class FuelType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип топлива'
        verbose_name_plural = 'Типы топлива'
        ordering = ['-id']

    def __str__(self):
        return self.name


class CarColor(models.Model):
    name = models.CharField(max_length=255, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Car(models.Model):
    mark = models.ForeignKey(CarMark, on_delete=models.CASCADE, verbose_name='Марка', related_name='cars')
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Модель', related_name='cars')
    year = models.PositiveSmallIntegerField(choices=year_choices, verbose_name='Год')
    horse_power = models.PositiveSmallIntegerField(choices=horse_power_choice, verbose_name='Лошадиные силы')
    seat = models.IntegerField(choices=SEAT_CHOICES, verbose_name='Кол-во сидений')
    body = models.ForeignKey(CarBody, on_delete=models.CASCADE, verbose_name='Тип кузова', related_name='cars')
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE, verbose_name='Тип топлива', related_name='cars')
    mileage = models.PositiveIntegerField(verbose_name='Пробег (км)')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за день', default=0)
    transmission = models.CharField(max_length=50, verbose_name='Коробка передач', choices=TRANSMISSION_CHOICES)
    drive_type = models.CharField(max_length=50, verbose_name='Привод', choices=DRIVE_TYPE_CHOICES)
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Объем двигателя (л)', null=True,
                                        blank=True)
    color = models.ForeignKey(CarColor, on_delete=models.CASCADE, verbose_name='Цвет', related_name='cars')
    description = models.TextField(verbose_name='Описание', blank=True)
    preview_img = models.ImageField(upload_to='cars/', verbose_name='Превью фото', null=True, blank=True)
    is_available = models.BooleanField(default=True, verbose_name='Доступна для аренды')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.mark.name} {self.model.name} ({self.year})"

    @property
    def full_name(self):
        return f"{self.mark.name} {self.model.name} {self.year}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images', verbose_name='Автомобиль')
    image = models.ImageField(upload_to='cars/', verbose_name='Фото')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Фото автомобиля'
        verbose_name_plural = 'Фото автомобилей'
        ordering = ['order']

    def __str__(self):
        return f"Фото {self.car.full_name}"


class Rent(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rents', verbose_name='Авто')
    rent_start = models.DateField(verbose_name='Дата начала аренды')
    rent_end = models.DateField(verbose_name='Дата окончания аренды')
    status = models.CharField(max_length=20, choices=RENT_STATUS_CHOICES, default='pending', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', null=True,
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ['-created_at']

    def __str__(self):
        return f"Аренда {self.car} с {self.rent_start} по {self.rent_end}"

    def save(self, *args, **kwargs):
        if self.rent_start and self.rent_end and self.car:
            days = (self.rent_end - self.rent_start).days + 1
            self.total_price = self.car.price_per_day * days
        super().save(*args, **kwargs)
