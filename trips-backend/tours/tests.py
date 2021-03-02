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
                            base_price=500.00,
                            departure_country="Poland",
                            departure_city="Poznań",
                            duration_days="1")

        tour2 = create_tour(destination="Płock",
                            country="Poland",
                            max_participants=15,
                            short_description="Zwiedzianie",
                            long_description="Zwiedzanie wspaniałego miasta, jakim jest Plock.",
                            base_price=500.00,
                            departure_country="Poland",
                            departure_city="Poznań",
                            duration_days="1")
        return [tour1, tour2]

    def test_route_get_all(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_route_get_all_not_return_base_price(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert not any("base_price" in tour for tour in response.json())

    def test_route_get_one(self, client, two_tours):
        id_ = two_tours[0].id
        response = client.get(reverse('tour-detail', args=[id_]), follow=True)

        assert response.status_code == 200
        assert response.json()['destination'] == "Poznań"

    def test_route_get_one_not_return_base_price(self, client, two_tours):
        id_ = two_tours[0].id
        response = client.get(reverse('tour-detail', args=[id_]), follow=True)

        assert response.status_code == 200
        assert not "base_price" in response.json()
