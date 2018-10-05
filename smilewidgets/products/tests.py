from collections import namedtuple

from rest_framework import status
from rest_framework.test import APITestCase

Parameters = namedtuple('Parameters', 'product_code date gift_card_code')


class GetPriceTestCase(APITestCase):
    fixtures = ['0002_fixtures.json']

    def test_default_prices(self):
        for parameters, expected_response in {
            Parameters(product_code='sm_widget', date='2018-09-05', gift_card_code=None): 9900,
            Parameters(product_code='big_widget', date='2018-10-20', gift_card_code=None): 100000,
            Parameters(product_code='sm_widget', date='2018-08-03', gift_card_code='10OFF'): 8900,
            Parameters(product_code='big_widget', date='2018-12-05', gift_card_code='250OFF'): 75000,
        }.items():
            with self.subTest(parameters=parameters, expected_response=expected_response):
                response = self.client.get('/api/get-price', {
                    key: value for key, value in parameters._asdict().items() if value is not None
                })
                self.assertEqual(response.data, expected_response)

    def test_black_friday_prices(self):
        for parameters, expected_response in {
            Parameters(product_code='sm_widget', date='2018-10-23', gift_card_code=None): 0,
            Parameters(product_code='big_widget', date='2018-10-24', gift_card_code=None): 80000,
            Parameters(product_code='sm_widget', date='2018-10-25', gift_card_code='10OFF'): 0,
            Parameters(product_code='big_widget', date='2018-10-24', gift_card_code='50OFF'): 75000,
        }.items():
            with self.subTest(parameters=parameters, expected_response=expected_response):
                response = self.client.get('/api/get-price', {
                    key: value for key, value in parameters._asdict().items() if value is not None
                })
                self.assertEqual(response.data, expected_response)

    def test_2019_prices(self):
        for parameters, expected_response in {
            Parameters(product_code='sm_widget', date='2019-01-12', gift_card_code=None): 12500,
            Parameters(product_code='big_widget', date='2019-05-07', gift_card_code=None): 120000,
            Parameters(product_code='sm_widget', date='2019-03-21', gift_card_code='50OFF'): 7500,
            Parameters(product_code='big_widget', date='2019-10-24', gift_card_code='10OFF'): 119000,
        }.items():
            with self.subTest(parameters=parameters, expected_response=expected_response):
                response = self.client.get('/api/get-price', {
                    key: value for key, value in parameters._asdict().items() if value is not None
                })
                self.assertEqual(response.data, expected_response)

    def test_bad_product_code(self):
        response = self.client.get('/api/get-price', {
            'product_code': 'medium_widget',
            'date': '2018-10-04'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'error': 'No such product'
        })

    def test_bad_gift_card_code(self):
        response = self.client.get('/api/get-price', {
            'product_code': 'sm_widget',
            'date': '2018-10-04',
            'gift_card_code': '15OFF'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
            'error': 'No such gift card'
        })

    def test_bad_date_format(self):
        response = self.client.get('/api/get-price', {
            'product_code': 'sm_widget',
            'date': '2018.10.04',
            'gift_card_code': '10OFF'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('Date has wrong format' in response.json().get('error', ''))

