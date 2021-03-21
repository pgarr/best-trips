from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Tour, Reservation, TourInstance


class TourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tour
        fields = ['url', 'id', 'destination', 'country', 'max_participants', 'short_description',
                  'long_description', 'departure_country', 'departure_city', 'duration_days', 'main_image']


class TourInstanceSerializer(serializers.ModelSerializer):
    tour = TourSerializer(read_only=True)

    class Meta:
        model = TourInstance
        fields = '__all__'


class ReservationBaseSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
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


class ReservationCreateSerializer(ReservationBaseSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, attrs):
        errors = dict()
        if not self.has_free_places(attrs):
            errors['num_people'] = 'Not enough free places'

        if errors:
            raise serializers.ValidationError(errors)
        return super(ReservationCreateSerializer, self).validate(attrs)

    def has_free_places(self, attrs):
        if self.instance:
            return not attrs['num_people'] > self.instance.tour_instance.free_places + self.instance.num_people
        else:
            return not attrs['num_people'] > attrs['tour_instance'].free_places


class ReservationListSerializer(ReservationBaseSerializer):
    departure_time = serializers.ReadOnlyField(source='tour_instance.departure_time')
    return_time = serializers.ReadOnlyField(source='tour_instance.return_time')
    tour_instance = serializers.StringRelatedField()

    class Meta:
        model = Reservation
        fields = ['url', 'id', 'num_people', 'confirmed', 'paid', 'owner', 'tour_instance', 'departure_time',
                  'return_time']
        validators = [
            UniqueTogetherValidator(
                queryset=Reservation.objects.all(),
                fields=['owner', 'tour_instance']
            )
        ]


class ReservationDetailSerializer(ReservationBaseSerializer):
    tour_instance = TourInstanceSerializer(read_only=True)
