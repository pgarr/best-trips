from rest_framework import serializers

from .models import Tour, Reservation


class TourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tour
        fields = ['url', 'id', 'destination', 'country', 'max_participants', 'short_description',
                  'long_description', 'departure_country', 'departure_city', 'duration_days']


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tour_instance = serializers.ReadOnlyField(source='tour_instance.__str()__')
    tour_instance_id = serializers.IntegerField(write_only=True)
    confirmed = serializers.ReadOnlyField()
    paid = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ['url', 'id', 'num_people', 'confirmed', 'paid', 'owner', 'tour_instance', 'tour_instance_id']
