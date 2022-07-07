import time

def response_mock(time: int = int(time.time()), time_next_update: int = int(time.time()) + 1000):
    return {
        "result": "success",
        "documentation": "https://www.exchangerate-api.com/docs",
        "terms_of_use": "https://www.exchangerate-api.com/terms",
        "time_last_update_unix": time,
        "time_last_update_utc": "Fri, 27 Mar 2020 00:00:00 +0000",
        "time_next_update_unix": time_next_update,
        "time_next_update_utc": "Sat, 28 Mar 2020 00:00:00 +0000",
        "base_code": "USD",
        "conversion_rates": {
            "USD": 1,
            "AUD": 1.4817,
            "BGN": 1.7741,
            "CAD": 1.3168,
            "CHF": 0.9774,
            "CNY": 6.9454,
            "EGP": 15.7361,
            "EUR": 0.9013,
            "GBP": 0.7679,
            "ILS": 0.28
	}
}
