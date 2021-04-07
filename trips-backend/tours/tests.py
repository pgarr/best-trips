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

    def test_get_all(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_all_not_return_base_price(self, client, two_tours):
        response = client.get(reverse('tour-list'), follow=True)

        assert response.status_code == 200
        assert not any('base_price' in tour for tour in response.json())

    def test_get_one(self, client, two_tours):
        id_ = two_tours[0].id
        response = client.get(reverse('tour-detail', args=[id_]), follow=True)

        assert response.status_code == 200
        assert response.json()['destination'] == 'Poznań'

    def test_get_one_not_return_base_price(self, client, two_tours):
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

        create_reservation(owner=user1,
                           tour_instance=one_tour_instance,
                           num_people=number_people_1,
                           confirmed=True,
                           paid=True)

        create_reservation(owner=user2,
                           tour_instance=one_tour_instance,
                           num_people=number_people_2,
                           confirmed=True,
                           paid=True)

        assert one_tour_instance.free_places == one_tour_instance.tour.max_participants - (
                number_people_1 + number_people_2)


@pytest.mark.django_db
class TestTourInstanceRoutes:
    @pytest.fixture
    def four_tour_instances(self, two_tours, create_tour_instance):
        first_june_instance = create_tour_instance(tour=two_tours[0],
                                                   departure_time=datetime.datetime(2020, 6, 17),
                                                   return_time=datetime.datetime(2020, 6, 19),
                                                   price=200)

        second_june_instance = create_tour_instance(tour=two_tours[1],
                                                    departure_time=datetime.datetime(2020, 6, 27),
                                                    return_time=datetime.datetime(2020, 6, 29),
                                                    price=200)

        first_may_instance = create_tour_instance(tour=two_tours[0],
                                                  departure_time=datetime.datetime(2020, 5, 17),
                                                  return_time=datetime.datetime(2020, 5, 19),
                                                  price=200)

        second_may_instance = create_tour_instance(tour=two_tours[1],
                                                   departure_time=datetime.datetime(2020, 5, 27),
                                                   return_time=datetime.datetime(2020, 5, 29),
                                                   price=200)

        return [first_may_instance, second_may_instance, first_june_instance, second_june_instance]

    def test_get_all(self, client, four_tour_instances):
        response = client.get(reverse('tourinstance-list'))
        assert len(response.json()) == 4

    def test_get_all_is_sorted_by_departure_time_asc(self, client, four_tour_instances):
        response = client.get(reverse('tourinstance-list'))

        instances = response.json()
        assert all(
            instances[i]['departure_time'] <= instances[i + 1]['departure_time'] for i in range(len(instances) - 1))

    def test_get_all_all_required_data(self, client, four_tour_instances):
        response = client.get(reverse('tourinstance-list'))

        instances = response.json()

        assert all('departure_time' in instance for instance in instances)
        assert all('return_time' in instance for instance in instances)
        assert all('price' in instance for instance in instances)
        assert all('tour' in instance for instance in instances)
        assert all('short_description' in instance['tour'] for instance in instances)
        assert all('main_image' in instance['tour'] for instance in instances)
        assert all('destination' in instance['tour'] for instance in instances)
        assert all('country' in instance['tour'] for instance in instances)

    def test_get_all_filter_by_departure_date(self, client, four_tour_instances):
        response = client.get(reverse('tourinstance-list'), {'departure_time_after': '2020-06-01'})
        assert len(response.json()) == 2


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
        create_reservation(owner=user1,
                           tour_instance=full_booked_inst,
                           num_people=full_booked_inst.tour.max_participants,
                           confirmed=True,
                           paid=True)

        three_places_inst = create_tour_instance(tour=tour2,
                                                 departure_time=datetime.datetime(2020, 5, 17),
                                                 return_time=datetime.datetime(2020, 5, 19),
                                                 price=200)
        create_reservation(owner=user1,
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

        assert response.status_code == 401

    def test_create_reservation_fail_people_less_then_one(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        access = create_token(user2)['access']

        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 0,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert 'num_people' in response.json()

    def test_create_reservation_fail_without_data(self, client, two_users, three_instances, create_token):
        user1, user2 = two_users
        access = create_token(user2)['access']

        response = client.post(reverse('reservation-list'), HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert 'num_people' in response.json()
        assert 'tour_instance' in response.json()

    def test_create_reservation_fail_without_num_people(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_places_inst.id,
                            }
        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert 'num_people' in response.json()

    def test_create_reservation_fail_without_tour_instance(self, client, two_users, three_instances, create_token):
        user1, user2 = two_users
        access = create_token(user2)['access']
        reservation_data = {'num_people': 2,
                            }
        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert 'tour_instance' in response.json()

    def test_create_reservation_success_properly_set_data(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 2,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 201
        new_reservation = Reservation.objects.get(tour_instance=full_places_inst)
        assert new_reservation.owner == user2
        assert not new_reservation.confirmed
        assert not new_reservation.paid

    def test_create_reservation_success_dont_override_owner(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        access = create_token(user2)['access']
        reservation_data = {'tour_instance': full_places_inst.id,
                            'num_people': 2,
                            'owner': user1.id
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 201
        new_reservation = Reservation.objects.get(tour_instance=full_places_inst)
        assert new_reservation.owner == user2

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

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

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

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert 'num_people' in response.json()

    def test_create_reservation_fail_too_few_free_places(self, client, two_users, three_instances, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        access = create_token(user2)['access']
        reservation_data = {'tour_instance': three_places_inst.id,
                            'num_people': 4,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert 'num_people' in response.json()

    def test_create_reservation_fail_user_has_reservation_already(self, client, two_users, three_instances,
                                                                  create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        access = create_token(user1)['access']
        reservation_data = {'tour_instance': three_places_inst.id,
                            'num_people': 2,
                            }

        response = client.post(reverse('reservation-list'), reservation_data, HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400

    def test_get_reservation_list_fail_without_token(self, client, three_instances):
        response = client.get(reverse('reservation-list'))

        assert response.status_code == 401

    def test_get_reservation_list_success_two_reservations_user(self, client, two_users, three_instances, create_token):
        user1, user2 = two_users
        access = create_token(user1)['access']

        response = client.get(reverse('reservation-list'), HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_reservation_list_success_all_have_required_fields(self, client, two_users, three_instances,
                                                                   create_token):
        user1, user2 = two_users
        access = create_token(user1)['access']

        response = client.get(reverse('reservation-list'), HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200
        assert all('departure_time' in instance for instance in response.json())
        assert all('return_time' in instance for instance in response.json())
        assert all('tour_instance' in instance for instance in response.json())
        assert all('confirmed' in instance for instance in response.json())
        assert all('paid' in instance for instance in response.json())
        assert all('owner' in instance for instance in response.json())

    def test_get_reservation_list_success_no_reservations_user(self, client, two_users, three_instances, create_token):
        user1, user2 = two_users
        access = create_token(user2)['access']

        response = client.get(reverse('reservation-list'), HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_delete_reservation_fail_without_token(self, client, two_users, three_instances, create_reservation):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        response = client.delete(reverse('reservation-detail', args=[reservation.id]))
        assert response.status_code == 401

    def test_delete_reservation_fail_with_wrong_token(self, client, two_users, three_instances, create_reservation,
                                                      create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        access = create_token(user1)['access']
        response = client.delete(reverse('reservation-detail', args=[reservation.id]),
                                 HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 403

    def test_delete_reservation_success(self, client, two_users, three_instances, create_reservation,
                                        create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        access = create_token(user2)['access']
        response = client.delete(reverse('reservation-detail', args=[reservation.id]),
                                 HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 204
        reservations = Reservation.objects.filter(tour_instance=full_places_inst)
        assert not reservations

    def test_get_reservation_fail_without_token(self, client, two_users, three_instances, create_reservation):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        response = client.get(reverse('reservation-detail', args=[reservation.id]))
        assert response.status_code == 401

    def test_get_reservation_fail_with_wrong_token(self, client, two_users, three_instances, create_reservation,
                                                   create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        access = create_token(user1)['access']
        response = client.get(reverse('reservation-detail', args=[reservation.id]),
                              HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 403

    def test_get_reservation_success(self, client, two_users, three_instances, create_reservation,
                                     create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        access = create_token(user2)['access']
        response = client.get(reverse('reservation-detail', args=[reservation.id]),
                              HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200

    def test_get_reservation_success_has_required_data(self, client, two_users, three_instances, create_reservation,
                                                       create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)

        access = create_token(user2)['access']
        response = client.get(reverse('reservation-detail', args=[reservation.id]),
                              HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200
        assert 'num_people' in response.json()
        assert 'confirmed' in response.json()
        assert 'paid' in response.json()
        assert 'tour_instance' in response.json()
        tour_instance = response.json()['tour_instance']

        assert 'departure_time' in tour_instance
        assert 'return_time' in tour_instance
        assert 'additional_info' in tour_instance
        assert 'price' in tour_instance
        assert 'tour' in tour_instance
        tour = tour_instance['tour']

        assert 'destination' in tour
        assert 'country' in tour
        assert 'max_participants' in tour
        assert 'short_description' in tour
        assert 'long_description' in tour
        assert 'base_price' not in tour
        assert 'departure_country' in tour
        assert 'departure_city' in tour

    def test_update_reservation_fail_without_token(self, client, two_users, three_instances,
                                                   create_reservation):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        update_data = {
            'num_people': 2,
        }

        response = client.put(reverse('reservation-detail', args=[reservation.id]), update_data)
        assert response.status_code == 401

    def test_update_reservation_fail_with_wrong_token(self, client, two_users, three_instances,
                                                      create_reservation, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        update_data = {
            'num_people': 2,
        }
        access = create_token(user1)['access']

        response = client.put(reverse('reservation-detail', args=[reservation.id]), update_data,
                              HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 403

    def test_update_reservation_fail_no_data(self, client, two_users, three_instances, create_reservation,
                                             create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        access = create_token(user2)['access']

        response = client.put(reverse('reservation-detail', args=[reservation.id]),
                              HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400

    def test_update_reservation_fail_not_enough_free_places(self, client, two_users, three_instances,
                                                            create_reservation, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users

        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        update_data = {
            'num_people': 16,
        }
        access = create_token(user2)['access']

        response = client.put(reverse('reservation-detail', args=[reservation.id]), update_data,
                              'application/json', HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 400
        assert not reservation.num_people == update_data['num_people']

    def test_update_reservation_success_enough_free_places(self, client, two_users, three_instances,
                                                           create_reservation, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        update_data = {
            'num_people': 15,
        }
        access = create_token(user2)['access']

        response = client.put(reverse('reservation-detail', args=[reservation.id]), update_data,
                              'application/json', HTTP_AUTHORIZATION='Bearer %s' % access)

        reservation.refresh_from_db()
        assert response.status_code == 200
        assert reservation.num_people == update_data['num_people']

    def test_update_reservation_success_dont_override_owner(self, client, two_users, three_instances,
                                                            create_reservation, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        update_data = {
            'num_people': 15,
            'owner': user1.id
        }
        access = create_token(user2)['access']

        response = client.put(reverse('reservation-detail', args=[reservation.id]), update_data,
                              'application/json', HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200
        assert reservation.owner == user2

    def test_update_reservation_success_dont_override_tour_instance(self, client, two_users, three_instances,
                                                                    create_reservation, create_token):
        full_booked_inst, three_places_inst, full_places_inst = three_instances
        user1, user2 = two_users
        reservation = create_reservation(owner=user2,
                                         tour_instance=full_places_inst,
                                         num_people=1,
                                         confirmed=False,
                                         paid=False)
        update_data = {
            "num_people": 1,
            "tour_instance": three_places_inst.id,
        }
        access = create_token(user2)['access']

        response = client.put(reverse('reservation-detail', args=[reservation.id]), update_data,
                              'application/json', HTTP_AUTHORIZATION='Bearer %s' % access)

        assert response.status_code == 200
        assert reservation.tour_instance == full_places_inst
