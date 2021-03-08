import pytest

from tours.models import Tour, TourInstance, Reservation
from django.contrib.auth.models import User


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_tour(db):
    def make_tour(**kwargs):
        return Tour.objects.create(**kwargs)

    return make_tour


@pytest.fixture
def create_tour_instance(db):
    def make_tour_instance(**kwargs):
        return TourInstance.objects.create(**kwargs)

    return make_tour_instance


@pytest.fixture
def create_reservation(db):
    def make_reservation(**kwargs):
        return Reservation.objects.create(**kwargs)

    return make_reservation
