from django.db import models
from django.core.validators import *


class CarSeller(models.Model):
    POOR = 'P'
    FAIR = 'F'
    GOOD = 'G'
    EXCELLENT = 'E'
    CHOICES = (
        (POOR, "poor"),
        (FAIR, "fair"),
        (GOOD, "good"),
        (EXCELLENT,'excellent'),
    )
    seller_name = models.CharField(max_length=20)
    seller_mobile = models.CharField(max_length = 10, validators = [MinLengthValidator(10), MaxLengthValidator(10)])
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(default=0)
    Condition = models.CharField(max_length=10, choices= CHOICES)
    asking_pricce = models.FloatField(max_length=7)
    picture = models.ImageField(upload_to="media/",null=False)
    
    def __str__(self):
        return self.seller_name