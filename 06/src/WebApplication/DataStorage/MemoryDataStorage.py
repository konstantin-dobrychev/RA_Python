import uuid

from typing import AsyncIterable

from DataStorage.DataStorage import DataStorage


class MemoryDataStorage(DataStorage):
    def __init__(self):
        self.__storage = {}

    async def get_objects(self) -> AsyncIterable:
        for value in self.__storage.values():
            yield value

    async def get_object(self, key: uuid) -> dict:
        return self.__storage.get(key)

    async def put_object(self, key: uuid, value: dict):
        self.__storage[key] = value

    async def delete_object(self, key: uuid):
        self.__storage.pop(key)
