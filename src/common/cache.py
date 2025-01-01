from typing import Union, Any


class Cache:
    """
    Cache class that used to cache the data.
    """

    def __init__(self):
        self.data: dict = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key, None)

    def has(self, key: str) -> bool:
        return key in self.data

    def clear(self):
        self.data = {}


cacher = Cache()
