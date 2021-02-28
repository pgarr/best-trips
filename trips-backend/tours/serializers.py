from rest_framework import serializers

from .models import Tour


class TourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tour
        fields = ['url', 'destination', 'country', 'max_participants', 'short_description',
                  'long_description', 'price', 'start_date', 'end_date']
