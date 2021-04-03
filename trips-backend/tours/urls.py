from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'tours', views.TourViewSet)
router.register(r'reservations', views.ReservationViewSet)
router.register(r'instances', views.TourInstanceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
