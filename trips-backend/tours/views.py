from rest_framework import viewsets

from .serializers import TourSerializer
from .models import Tour


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.all().order_by('-created')
    serializer_class = TourSerializer
