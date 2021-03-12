from rest_framework import permissions, viewsets

from .serializers import TourSerializer, ReservationSerializer
from .models import Tour, Reservation, TourInstance


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.all().order_by('-created')
    serializer_class = TourSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        tour_inst = TourInstance.objects.get(id=serializer.validated_data['tour_instance_id'])
        serializer.save(owner=self.request.user, tour_instance=tour_inst)
