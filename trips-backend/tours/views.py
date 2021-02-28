from rest_framework import viewsets

from .serializers import TourSerializer
from .models import Tour


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.all().order_by('-start_date')
    serializer_class = TourSerializer
