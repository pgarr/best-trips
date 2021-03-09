from rest_framework import viewsets

from .serializers import TourSerializer, ReservationSerializer
from .models import Tour, Reservation


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.all().order_by('-created')
    serializer_class = TourSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
