from django.db import models
from .choices import year_choices, SEAT_CHOICES, horse_power_choice


class CarMark(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марка'
        ordering = ['-id']

    def __str__(self):
        return self.name

class CarBody(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Тип кузова'
        ordering = ['-id']

    def __str__(self):
        return self.name

class CarModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модель'
        ordering = ['-id']

class FuelType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    class Meta:
        verbose_name = 'Тип топлива'
        verbose_name_plural = 'Тип топлива'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Car(models.Model):
    mark = models.ForeignKey(CarMark, on_delete=models.CASCADE, verbose_name='Марка')
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name='Модель')
    year = models.PositiveSmallIntegerField(choices=year_choices, verbose_name='Год')
    horse_power = models.PositiveSmallIntegerField(choices=horse_power_choice,verbose_name='ХЫПЫ')
    seat = models.IntegerField(choices=SEAT_CHOICES, verbose_name='кл-во сидений')
    body = models.ForeignKey(CarBody, on_delete=models.CASCADE, verbose_name='Тип кузова')
    mileage = models.PositiveIntegerField(verbose_name='Пробег')
    preview_img = models.ImageField(upload_to='cars/', verbose_name='Превью фото', null=True, blank=True)

    def __str__(self):
        return f"{self.mark.name} - {self.model.name}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')

    class Meta:
        verbose_name = 'Превью фото'
        verbose_name_plural = 'Превью фото'


class Rent(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rents', verbose_name='Авто')
    rent_start = models.DateField(verbose_name='Дата начала аренды')
    rent_end = models.DateField(verbose_name='Дата окончания аренды')

    def __str__(self):
        return f"Аренда {self.car} с {self.rent_start} по {self.rent_end}"

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
