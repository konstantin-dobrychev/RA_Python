import uuid

from typing import AsyncIterable

from motor.motor_asyncio import AsyncIOMotorClient

from DataStorage import DataStorage


class MongoDataStorage(DataStorage):
    def __init__(self):
        self.__client = AsyncIOMotorClient()
        self.__collection = None

    async def create(self, database: str, collection: str):
        self.__collection = self.__client[database][collection]

    async def get_objects(self) -> AsyncIterable:
        async for value in self.__collection.find():
            yield self.__value(value)

    async def get_object(self, key: uuid) -> dict:
        return self.__value(await self.__collection.find_one({'_id': str(key)}))

    async def put_object(self, key: uuid, value: dict):
        value['_id'] = str(key)
        await self.__collection.find_one_and_replace({'_id': str(key)}, value, upsert=True)

    async def delete_object(self, key: uuid):
        await self.__collection.delete_one({'_id': str(key)})

    @staticmethod
    def __value(value: dict):
        if value:
            value['key'] = value.pop('_id')

        return value
