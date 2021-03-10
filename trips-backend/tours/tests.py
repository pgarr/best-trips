import datetime

import pytest
from django.urls import reverse

from tours.models import Reservation


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


@pytest.fixture
def two_users(create_user):
    user1 = create_user(username='test1',
                        email='test1@test.pl',
                        password='test456&')
    user2 = create_user(username='test2',
                        email='test2@test.pl',
                        password='test456&')
    return [user1, user2]


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

    def test_free_places_with_reservations(self, two_users, one_tour_instance, create_reservation):
        user1, user2 = two_users

        number_people_1 = 2
        number_people_2 = 3

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


@pytest.mark.django_db
class TestReservationRoutes:

    @pytest.fixture
    def three_instances(self, two_tours, two_users, create_tour_instance, create_reservation):
        tour1, tour2 = two_tours
        user1, user2 = two_users

        full_booked_inst = create_tour_instance(tour=tour1,
                                                departure_time=datetime.datetime(2020, 5, 17),
                                                return_time=datetime.datetime(2020, 5, 19),
                                                price=200)
        create_reservation(user=user1,
                           tour_instance=full_booked_inst,
                           num_people=full_booked_inst.tour.max_participants,
                           confirmed=True,
                           paid=True)

        three_places_inst = create_tour_instance(tour=tour2,
                                                 departure_time=datetime.datetime(2020, 5, 17),
                                                 return_time=datetime.datetime(2020, 5, 19),
                                                 price=200)
        create_reservation(user=user1,
                           tour_instance=three_places_inst,
                           num_people=three_places_inst.tour.max_participants - 3,
                           confirmed=True,
                           paid=True)

        full_places_inst = create_tour_instance(tour=tour2,
                                                departure_time=datetime.datetime(2020, 5, 17),
                                                return_time=datetime.datetime(2020, 5, 19),
                                                price=200)

        return full_booked_inst, three_places_inst, full_places_inst

    def test_create_reservation_fail_without_token(self, client, three_instances):
        full_booked_inst, three_places_inst, full_places_inst = three_instances

        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 2,
                            }

        response = client.post(reverse('reservation-list'), reservation_data)

        print(response.json())
        assert response.status_code == 401

    def test_create_reservation_fail_without_data(self, client, two_users, three_instances, create_token):
        user1, user2 = two_users

        access = create_token(user2)['access']

        response = client.post(reverse('reservation-list'), {}, HTTP_Authorization='Bearer %s' % access)

        assert response.status_code == 400

    def test_create_reservation_success_properly_set_data(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 2,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_Authorization='Bearer %s' % access)
        assert response.status_code == 201

        new_reservation = Reservation.objects.get(tour_instance=full_places_inst)
        assert new_reservation.user == user2
        assert not new_reservation.confirmed
        assert not new_reservation.paid

    def test_create_reservation_success_dont_override_user(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 2,
                            'user': user1.id
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_Authorization='Bearer %s' % access)
        assert response.status_code == 201

        new_reservation = Reservation.objects.get(tour_instance=full_places_inst)
        assert new_reservation.user == user2

    def test_create_reservation_success_dont_override_confirmed_and_paid(self, client, two_users, three_instances,
                                                                         create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 2,
                            'confirmed': True,
                            'paid': True
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_Authorization='Bearer %s' % access)
        assert response.status_code == 201

        new_reservation = Reservation.objects.get(tour_instance=full_places_inst)
        assert not new_reservation.confirmed
        assert not new_reservation.paid

    def test_create_reservation_fail_no_free_places(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_booked_inst.id,
                            'num_people': 2,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_Authorization='Bearer %s' % access)
        assert response.status_code == 422
        assert 'num_people' in response.json()['error']

    def test_create_reservation_fail_too_few_free_places(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        access = create_token(user2)['access']
        reservation_data = {'tour_instance': three_places_inst.id,
                            'num_people': 4,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_Authorization='Bearer %s' % access)
        assert response.status_code == 422
        assert 'num_people' in response.json()['error']

    def test_create_reservation_fail_user_has_reservation_already(self, client, two_users, three_instances,
                                                                  create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        access = create_token(user1)['access']
        reservation_data = {'tour_instance': three_places_inst.id,
                            'num_people': 2,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_Authorization='Bearer %s' % access)
        assert response.status_code == 422
        assert 'user' in response.json()['error']
