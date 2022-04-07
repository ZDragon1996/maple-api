from string import digits
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class US_State(models.Model):
    state_code = models.CharField(max_length=2, null=False, unique=True)
    state_name = models.CharField(max_length=50, null=False, unique=True)


class US_CITY(models.Model):
    city_name = models.CharField(max_length=50, null=False)
    county_name = models.CharField(max_length=50, null=False)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    state = models.ForeignKey(US_State, on_delete=models.CASCADE)
