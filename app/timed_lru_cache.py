import time


class TimedLRUCache:
    def __init__(self, fetch_func):
        self.items = dict()
        self.fetch_func = fetch_func

    def __call__(self, currency, *args):
        return self.get_or_fetch(currency)

    def get_or_fetch(self, currency: str):
        if currency not in self.items or self.items[currency].time_next_update_unix < int(time.time()):
            self._set(currency)

        return self.items[currency]

    def _set(self, currency: str, retry: int = 0):
        result = self.fetch_func(currency)

        if result.time_next_update_unix < int(time.time()) and retry == 0:
            return self._set(currency, 1)

        if currency in self.items and result.time_next_update_unix < self.items[currency].time_next_update_unix:
            return

        self.items[currency] = result
