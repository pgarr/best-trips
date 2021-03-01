import pytest

from tours.models import Tour


@pytest.fixture
def create_tour(db):
    def make_tour(**kwargs):
        return Tour.objects.create(**kwargs)

    return make_tour
