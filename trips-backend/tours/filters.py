from django_filters import rest_framework as filters, DateFromToRangeFilter

from .models import TourInstance


class TourInstanceFilter(filters.FilterSet):
    departure_time = DateFromToRangeFilter()

    class Meta:
        model = TourInstance
        fields = ['departure_time']
