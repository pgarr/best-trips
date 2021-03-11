from rest_framework import serializers

from .models import Tour, Reservation


class TourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tour
        fields = ['url', 'destination', 'country', 'max_participants', 'short_description',
                  'long_description', 'departure_country', 'departure_city', 'duration_days']


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reservation
        fields = ['url', 'num_people', 'confirmed', 'paid']
