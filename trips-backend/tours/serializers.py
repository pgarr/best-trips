from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Tour, Reservation, TourInstance


class TourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tour
        fields = ['url', 'id', 'destination', 'country', 'max_participants', 'short_description',
                  'long_description', 'departure_country', 'departure_city', 'duration_days']


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tour_instance = serializers.PrimaryKeyRelatedField(queryset=TourInstance.objects.all())
    confirmed = serializers.ReadOnlyField()
    paid = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ['url', 'id', 'num_people', 'confirmed', 'paid', 'owner', 'tour_instance']
        validators = [
            UniqueTogetherValidator(
                queryset=Reservation.objects.all(),
                fields=['owner', 'tour_instance']
            )
        ]
