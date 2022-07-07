from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json
@dataclass
class CurrencyConversionRateResponse:
    time_next_update_unix: int
    conversion_rates: dict

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QuoteExchangeAmount:
    exchange_rate: int
    quote_amount: int
