import datetime

SEAT_CHOICES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def horse_power_choice():
    return [(r,r) for r in range(100, 1000 + 1)]