from django.core.validators import MinValueValidator
from django.db import models


class Tour(models.Model):
    destination = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    max_participants = models.IntegerField(validators=[MinValueValidator])
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def get_place(self):
        return '%s, %s' % (self.country, self.destination)

    def __str__(self):
        return '%s - %s' % (self.get_place(), self.short_description)
