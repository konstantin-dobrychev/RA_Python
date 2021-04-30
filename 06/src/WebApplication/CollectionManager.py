from typing import List

from DataStorage import DataStorage, DataStorageFactory


class CollectionManager(object):
    def __init__(self, collections: List[str], storage_settings: dict):
        self.__collections = collections
        self.__storage_settings = storage_settings
        self.__storages = {}

    def collections(self) -> List[str]:
        return self.__collections

    async def data_storage(self, collection: str) -> DataStorage:
        if collection not in self.__storages:
            self.__storages[collection] = await self.__create_data_storage(collection)

        return self.__storages[collection]

    async def __create_data_storage(self, collection: str) -> DataStorage:
        self.__storage_settings['collection'] = collection
        return await DataStorageFactory.create_storage(self.__storage_settings)
