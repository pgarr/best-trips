import datetime

import pytest
from django.urls import reverse


@pytest.fixture
def two_tours(create_tour):
    tour1 = create_tour(destination="Poznań",
                        country="Poland",
                        max_participants=15,
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


@pytest.mark.django_db
class TestTourRoutes:

    def test_route_get_all(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_route_get_all_not_return_base_price(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert not any('base_price' in tour for tour in response.json())

    def test_route_get_one(self, client, two_tours):
        id_ = two_tours[0].id
        response = client.get(reverse('tour-detail', args=[id_]), follow=True)

        assert response.status_code == 200
        assert response.json()['destination'] == 'Poznań'

    def test_route_get_one_not_return_base_price(self, client, two_tours):
        id_ = two_tours[0].id
        response = client.get(reverse('tour-detail', args=[id_]), follow=True)

        assert response.status_code == 200
        assert 'base_price' not in response.json()


@pytest.mark.django_db
class TestTourInstanceModel:
    @pytest.fixture
    def one_tour_instance(self, two_tours, create_tour_instance):
        tour_instance = create_tour_instance(tour=two_tours[0],
                                             departure_time=datetime.datetime(2020, 5, 17),
                                             return_time=datetime.datetime(2020, 5, 19),
                                             price=200)
        return tour_instance

    def test_free_places_no_reservations(self, one_tour_instance):
        assert one_tour_instance.free_places == one_tour_instance.tour.max_participants

    def test_free_places_with_reservations(self, create_user, one_tour_instance, create_reservation):
        number_people_1 = 2
        number_people_2 = 3

        user1 = create_user(username='test1',
                            email='test1@test.pl',
                            password='test456&')
        user2 = create_user(username='test2',
                            email='test2@test.pl',
                            password='test456&')

        create_reservation(user=user1,
                           tour_instance=one_tour_instance,
                           num_people=number_people_1,
                           confirmed=True,
                           paid=True)

        create_reservation(user=user2,
                           tour_instance=one_tour_instance,
                           num_people=number_people_2,
                           confirmed=True,
                           paid=True)

        assert one_tour_instance.free_places == one_tour_instance.tour.max_participants - (
                    number_people_1 + number_people_2)
