from django.test import TestCase
from django.test import Client

from .models import Tour


# TODO: pytest
class TourTestCase(TestCase):

    def setUp(self):
        Tour.objects.create(destination="Poznań",
                            country="Poland",
                            max_participants=1,
                            short_description="Wycieczka objazdowa",
                            long_description="Oglądanie miasta przez okno autobusu. Czy może być coś lepszego?",
                            price=500.00,
                            start_date="2021-03-28T11:00:00Z",
                            end_date="2021-03-28T19:00:00Z")
        Tour.objects.create(destination="Płock",
                            country="Poland",
                            max_participants=15,
                            short_description="Zwiedzianie",
                            long_description="Zwiedzanie wspaniałego miasta, jakim jest Plock.",
                            price=500.00,
                            start_date="2021-02-28T11:00:00Z",
                            end_date="2021-02-28T15:00:00Z")

    def test_route_get_all(self):
        c = Client()
        response = c.get('/api/v1/tours/tours', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_route_get_one(self):
        c = Client()
        response = c.get('/api/v1/tours/tours/3', follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['destination'], "Poznań")
