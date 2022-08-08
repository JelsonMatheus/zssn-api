from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Survivor(models.Model):
    GENDER_CHOICES = (
        ("F", "Feminine"),
        ("M", "Masculine")
    )

    name = models.CharField(max_length=120)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_infected = models.BooleanField(default=False)
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
    class ItemValue(models.IntegerChoices):
        WATER = 4,
        FOOD = 3
        MEDICATION = 2
        AMMUNITION = 1

    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, primary_key=True)
    water = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    medication = models.IntegerField(default=0)
    ammunition = models.IntegerField(default=0)

    def get_full_value_item(self, name):
        unit_value = getattr(self.ItemValue, name.upper())
        return getattr(self, name) * unit_value

    @property
    def total_resource_value(self):
        item_names = [label.lower() for label in self.ItemValue.labels]
        value = 0
        for name in item_names:
            value += self.get_full_value_item(name)
        return value


class InfectedReport(models.Model):
    informant = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='reports')
    infected = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='reported')
    date_report = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('informant', 'infected')
