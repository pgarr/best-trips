import pytest

from tours.models import Tour
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
