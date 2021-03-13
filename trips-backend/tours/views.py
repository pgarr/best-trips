from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Tour, Reservation
from .permissions import IsOwner
from .serializers import TourSerializer, ReservationSerializer


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.all().order_by('-created')
    serializer_class = TourSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'destroy', 'partial_update']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        data = {**request.data.dict(),
                'owner': request.user.pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        user = request.user
        # override default queryset to filter by user
        self.queryset = Reservation.objects.filter(owner=user)
        return super(ReservationViewSet, self).list(request, *args, **kwargs)
