import time


class LRUCache:
    def __init__(self, fetch_func):
        self.items = dict()
        self.fetch_func = fetch_func

    def __call__(self, *args):
        return self.get(args[0])

    def get(self, currency: str):
        if currency not in self.items or self.items[currency].time_next_update_unix < int(time.time()):
            self.set(currency)

        return self.items[currency]

    def set(self, currency: str, retry: int = 0):
        result = self.fetch_func(currency)

        if result.time_next_update_unix < int(time.time()) and retry == 0:
            return self.set(currency, 1)

        if currency in self.items and result.time_next_update_unix < self.items[currency].time_next_update_unix:
            return

        self.items[currency] = result
