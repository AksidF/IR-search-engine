from typing import Union


class Cacher:
    """
    Cacher class that used to cache the data.
    """

    def __init__(self):
        self.data: dict = {}

    def set(self, key: str, value: str):
        self.data[key] = value

    def get(self, key: str) -> Union[str, None]:
        return self.data.get(key, None)

    def has(self, key: str) -> bool:
        return key in self.data