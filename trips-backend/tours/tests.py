import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestTourRoutes:

    @pytest.fixture
    def two_tours(self, create_tour):
        tour1 = create_tour(destination="Poznań",
                            country="Poland",
                            max_participants=1,
                            short_description="Wycieczka objazdowa",
                            long_description="Oglądanie miasta przez okno autobusu. Czy może być coś lepszego?",
                            price=500.00,
                            start_date="2021-03-28T11:00:00Z",
                            end_date="2021-03-28T19:00:00Z")

        tour2 = create_tour(destination="Płock",
                            country="Poland",
                            max_participants=15,
                            short_description="Zwiedzianie",
                            long_description="Zwiedzanie wspaniałego miasta, jakim jest Plock.",
                            price=500.00,
                            start_date="2021-02-28T11:00:00Z",
                            end_date="2021-02-28T15:00:00Z")
        return [tour1, tour2]

    def test_route_get_all(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_route_get_one(self, client, two_tours):
        id_ = two_tours[0].id
        response = client.get(reverse('tour-detail', args=[id_]), follow=True)

        assert response.status_code == 200
        assert response.json()['destination'] == "Poznań"
