import json
import os
import responses

from unittest import TestCase, mock
from app import create_app
from parameterized import parameterized
from .mock_data import response_mock


class TestQuoteCase(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @parameterized.expand([
        ('/quote', 'baseCurrency invalid value'),
        ('/quote?baseCurrency=ZZZ&quoteCurrency=GBP&baseAmount=1', 'baseCurrency invalid value'),
        ('/quote?quoteCurrency=GBP&baseAmount=1', 'baseCurrency invalid value'),
        ('/quote?baseCurrency=USD&baseAmount=1', 'quoteCurrency invalid value'),
        ('/quote?baseCurrency=USD&quoteCurrency=GBP', 'baseAmount invalid value'),
        ('/quote?baseCurrency=USD&quoteCurrency=GBP&baseAmount=FF', 'baseAmount invalid value'),
        ('/quote?baseCurrency=USD&quoteCurrency=GBP&baseAmount=-101', 'baseAmount invalid value'),
    ])
    def test_invalid_query(self, query_url, error_msg):
        response = self.client.get(query_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], error_msg)

    @responses.activate
    @mock.patch.dict(os.environ, {"api_key": "TEST_KEY"})
    def test_valid_query(self):
        responses.add(responses.GET, 'https://v6.exchangerate-api.com/v6/TEST_KEY/latest/USD', json=response_mock(), status=200)

        response = self.client.get('/quote?baseCurrency=USD&quoteCurrency=GBP&baseAmount=100')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['exchangeRate'], '0.768')
        self.assertEqual(data['quoteAmount'], '0.77')

    @responses.activate
    @mock.patch.dict(os.environ, {"api_key": "TEST_KEY"})
    def test_query_return_error(self):

        response_json = {"error-type": "unsupported-code"}
        responses.add(responses.GET, 'https://v6.exchangerate-api.com/v6/TEST_KEY/latest/USD', json=response_json, status=400)

        response = self.client.get('/quote?baseCurrency=USD&quoteCurrency=GBP&baseAmount=100')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'unsupported-code')
