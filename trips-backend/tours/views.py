from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .filters import TourInstanceFilter
from .models import Tour, Reservation, TourInstance
from .permissions import IsOwner
from .serializers import TourSerializer, ReservationBaseSerializer, ReservationCreateSerializer, \
    ReservationListSerializer, ReservationDetailSerializer, TourInstanceSerializer


class TourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tour.objects.all().order_by('-created')
    serializer_class = TourSerializer


class TourInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TourInstance.objects.all().order_by('departure_time')
    serializer_class = TourInstanceSerializer
    filterset_class = TourInstanceFilter


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationBaseSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'destroy', 'partial_update']:
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        self.serializer_class = ReservationCreateSerializer
        data = {**request.data.dict(),
                'owner': request.user.pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        self.serializer_class = ReservationListSerializer
        user = request.user
        # override default queryset to filter by user
        self.queryset = Reservation.objects.filter(owner=user)
        return super(ReservationViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ReservationDetailSerializer
        return super(ReservationViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ReservationCreateSerializer
        instance = self.get_object()
        data = {
            'num_people': request.data.get('num_people'),
            'owner': instance.owner.pk,
            'tour_instance': instance.tour_instance.pk
        }
        serializer = self.get_serializer(instance, data=data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
