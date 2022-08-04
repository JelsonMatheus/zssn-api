from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Survivor(models.Model):
    SEX_CHOICES = (
        ("F", "Feminine"),
        ("M", "Masculine")
    )

    name = models.CharField(max_length=120)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    latitude = models.DecimalField(
        max_digits=5, 
        decimal_places=3,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=6, 
        decimal_places=3,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )

    def __str__(self):
        self.name


class Inventory(models.Model):
    WATER_VALUE = 4
    FOOD_VALUE = 3
    MEDICATION = 2
    AMMUNITION = 1

    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, primary_key=True)
    water = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    medication = models.IntegerField(default=0)
    ammunition = models.IntegerField(default=0)

