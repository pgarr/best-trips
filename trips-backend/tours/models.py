from django.core.validators import MinValueValidator
from django.db import models


class Tour(models.Model):
    destination = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    max_participants = models.IntegerField(validators=[MinValueValidator(1)])
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()
    base_price = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
    departure_country = models.CharField(max_length=200)
    departure_city = models.CharField(max_length=200)
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])

    def get_destination(self):
        return '%s, %s' % (self.country, self.destination)

    def __str__(self):
        return '%s - %s' % (self.get_destination(), self.short_description)


class TourInstance(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    return_time = models.DateTimeField()
    additional_info = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s: from %s to %s' % (self.tour.get_destination(), self.departure_time, self.return_time)
