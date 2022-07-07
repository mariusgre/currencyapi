import time
from .mock_data import response_mock
from lru_cache import LRUCache
from models import CurrencyConversionRateResponse
from unittest import mock


def test_add_value_to_cache():
    func = mock.Mock(return_value = CurrencyConversionRateResponse.from_dict(response_mock()))
    cache = LRUCache(func)
    currency = 'USD'
    
    cache.get(currency)

    assert cache.items[currency].conversion_rates['GBP'] == 0.7679
    assert func.assert_called_once

def test_update_value_in_cache():
    current_time = int(time.time())
    last_time_updated = current_time - 100
    next_time_updated = current_time + 1000
    currency = 'USD'

    func = mock.Mock(return_value = CurrencyConversionRateResponse.from_dict(response_mock(last_time_updated, next_time_updated)))
    cache = LRUCache(func)

    cache.items[currency] = CurrencyConversionRateResponse.from_dict(response_mock(current_time - 1000, last_time_updated))
    
    cache.get(currency)

    assert cache.items[currency].time_next_update_unix == next_time_updated
    assert func.assert_called_once

def test_skip_update_value_to_cache():
    current_time = int(time.time())
    last_time_updated = current_time - 100
    next_time_updated = current_time + 1000
    currency = 'USD'

    func = mock.Mock(return_value = CurrencyConversionRateResponse.from_dict(response_mock(current_time - 1000, current_time - 100)))
    cache = LRUCache(func)

    cache.items[currency] = CurrencyConversionRateResponse.from_dict(response_mock(last_time_updated, next_time_updated))
    
    cache.get(currency)

    assert cache.items[currency].time_next_update_unix == next_time_updated
    assert not func.called

def test_retry_on_cache_update():
    current_time = int(time.time())
    last_time_updated = current_time - 1000
    next_time_updated = current_time - 100
    currency = 'USD'

    func = mock.Mock(return_value = CurrencyConversionRateResponse.from_dict(response_mock(last_time_updated, next_time_updated)))
    cache = LRUCache(func)

    cache.get(currency)

    assert cache.items[currency].time_next_update_unix == next_time_updated
    assert func.call_count == 2
