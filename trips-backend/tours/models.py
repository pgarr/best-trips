from django.core.validators import MinValueValidator
from django.db import models


class Tour(models.Model):
    destination = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.IntegerField(validators=[MinValueValidator])
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
