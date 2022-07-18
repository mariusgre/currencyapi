import os
import requests
from flask import Blueprint, request, make_response, jsonify
from decimal import Decimal

from models import CurrencyConversionRateResponse, QuoteExchangeAmount
from constants import API_BASE_URL, SUPPORTED_CURRENCIES
from status_codes import HTTP_400_BAD_REQUEST, HTTP_200_OK
from timed_lru_cache import TimedLRUCache
from utils import total_amount
from exceptions import CurrencyConversionApiException


quote_app = Blueprint('quote', __name__)


@quote_app.route('/quote', methods=['GET'])
def quote():
    try:
        args = request.args

        base_currency = args.get('baseCurrency')
        quote_currency = args.get('quoteCurrency')
        base_amount = args.get('baseAmount')

        if base_currency is None or base_currency.upper() not in SUPPORTED_CURRENCIES:
            return get_bad_request_response('baseCurrency invalid value')
        if quote_currency is None or quote_currency.upper() not in SUPPORTED_CURRENCIES:
            return get_bad_request_response('quoteCurrency invalid value')
        if base_amount is None or base_amount.isnumeric() is False or int(base_amount) <= 0:
            return get_bad_request_response('baseAmount invalid value')

        qoute_amount = _get_calculated_qoute(base_currency, quote_currency, int(base_amount))
        
        return make_response(qoute_amount.to_json(), HTTP_200_OK)

    except CurrencyConversionApiException as e:
        return get_error_response(e.message, e.status_code)
    except Exception as e:
        return get_error_response(e.response.reason, e.response.status_code)

def _get_calculated_qoute(base_currency: str, quote_currency: str, base_amount: int):
        currency_rates = _fetch_currency_conversion_rates(base_currency)
        exchange_rate = Decimal(currency_rates.conversion_rates[quote_currency])

        return QuoteExchangeAmount(exchange_rate = round(exchange_rate, 3), quote_amount = total_amount(int(base_amount), exchange_rate))

@TimedLRUCache
def _fetch_currency_conversion_rates(base_currency: str):
    try:
        url = f"{API_BASE_URL}/{os.getenv('api_key')}/latest/{base_currency}"
        r = requests.get(url)
        r.raise_for_status()
    except Exception as e:
        if 'error-type' in e.response.json():
            raise CurrencyConversionApiException(e.response.json()['error-type'], e.response.status_code)
        raise e

    return CurrencyConversionRateResponse.from_dict(r.json())

def get_bad_request_response(message: str):
    return get_error_response(message, HTTP_400_BAD_REQUEST)

def get_error_response(message: str, status_code: int):
    return make_response(jsonify({'error': message}), status_code)
