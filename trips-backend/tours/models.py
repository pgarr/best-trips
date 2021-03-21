from functools import reduce

from django.contrib.auth.models import User
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
    main_image = models.ImageField(upload_to='tours_main', blank=True)

    def __str__(self):
        return '%s, %s' % (self.country, self.destination)


class TourInstance(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT)
    departure_time = models.DateTimeField()
    return_time = models.DateTimeField()
    additional_info = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    @property
    def free_places(self):
        all_reservations = self.reservation_set.all()
        taken_places = reduce(lambda taken, reservation: taken + reservation.num_people, all_reservations, 0)
        return self.tour.max_participants - taken_places

    def __str__(self):
        return '%s: from %s to %s' % (self.tour, self.departure_time, self.return_time)


class Reservation(models.Model):
    class Meta:
        unique_together = ['owner', 'tour_instance']

    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    tour_instance = models.ForeignKey(TourInstance, on_delete=models.PROTECT)
    num_people = models.IntegerField(validators=[MinValueValidator(1)])
    confirmed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
