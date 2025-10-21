import datetime

SEAT_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

TRANSMISSION_CHOICES = [
    ('Механика', 'Механика'),
    ('Автомат', 'Автомат'),
    ('Электрический', 'Электрический'),
    ('Вариатор', 'Вариатор'),
    ('Робот', 'Робот')
]

DRIVE_TYPE_CHOICES = [
    ('Передний', 'Передний'),
    ('Задний', 'Задний'),
    ('Полный', 'Полный')
]

RENT_STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('active', 'Активна'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def horse_power_choice():
    return [(r,r) for r in range(100, 1000 + 1)]