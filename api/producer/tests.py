from decimal import Decimal

from .models import Producer, Crop
from rest_framework.test import APIClient, APITestCase


class ProducerTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.producer = Producer.objects.create(
            **{
                'register_number': '11144477735',
                'name': 'Roger That',
                'farm_name': 'Fazenda Dois',
                'city': 'Campinas',
                'state': 'SP',
                'total_area': round(Decimal(154), 2),
                'arable_area': round(Decimal(55), 2),
                'vegetation_area': round(Decimal(33), 2)
            }
        )
        self.crop_types = ['AL', 'CA', 'CN']

        for crop in self.crop_types:
            Crop.objects.create(
                type=crop,
                producer=self.producer
            )

    def test_list_producers(self):
        response = self.client.get('/producers/')
        self.assertEqual(response.status_code, 200)

    def test_create_producer(self):
        data = {
            'register_number': '11144477735',
            'name': 'New Producer',
            'crops': [
                {
                    'type': 'AL'
                },
                {
                    'type': 'CA'
                },
                {
                    'type': 'CN'
                }
            ],
            'farm_name': 'Fazenda Dois',
            'city': 'Campinas',
            'state': 'SP',
            'total_area': 154,
            'arable_area': 55,
            'vegetation_area': 33
        }
        response = self.client.post('/producers/', data, format='json')

        self.assertEqual(response.status_code, 201)

    def test_retrieve_producer(self):
        response = self.client.get(f'/producers/{self.producer.pk}/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['name'], self.producer.name)
        self.assertEqual(response.data['register_number'], self.producer.register_number)
        self.assertEqual(response.data['farm_name'], self.producer.farm_name)
        self.assertEqual(response.data['city'], self.producer.city)
        self.assertEqual(response.data['state'], self.producer.state)
        self.assertEqual(response.data['total_area'], str(self.producer.total_area))
        self.assertEqual(response.data['arable_area'], str(self.producer.arable_area))
        self.assertEqual(response.data['vegetation_area'], str(self.producer.vegetation_area))

        for crop in response.data['crops']:
            self.assertIn(crop['type'], self.crop_types)

    def test_update_producer(self):
        data = {
            'register_number': '11144477735',
            'name': 'Roger That',
            'crops': [
                {
                    'type': 'AL'
                },
                {
                    'type': 'CN'
                }
            ],
            'farm_name': 'New Farm',
            'city': 'Campinas',
            'state': 'SP',
            'total_area': 154,
            'arable_area': 55,
            'vegetation_area': 33
        }
        response = self.client.put(f'/producers/{self.producer.pk}/', data, format='json')
        self.assertEqual(response.status_code, 200)

        self.producer.refresh_from_db()

        self.assertEqual(data['register_number'], self.producer.register_number)
        self.assertEqual(data['name'], self.producer.name)
        self.assertEqual(data['farm_name'], self.producer.farm_name)

        for crop in response.data['crops']:
            self.assertIn(crop['type'], ['AL', 'CN'])

    def test_delete_producer(self):
        response = self.client.delete(f'/producers/{self.producer.pk}/')
        self.assertEqual(response.status_code, 204)
