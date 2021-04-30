import sqlite3
import uuid

from typing import AsyncIterable

from DataStorage import DataStorage


class SqliteDataStorage(DataStorage):
    def __init__(self):
        self.__collection = str()
        self.__connection = None
        self.__cursor = None

    async def create(self, filename: str, collection: str):
        self.__collection = collection
        self.__connection = sqlite3.connect(filename)
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.__collection} (
                key TEXT, original TEXT, translation TEXT, transcription TEXT
            )
        ''')

    async def get_objects(self) -> AsyncIterable:
        self.__cursor.execute(f'SELECT * FROM {self.__collection}')

        for row in self.__cursor:
            yield self.__extract_object(row)

    async def get_object(self, key: uuid) -> dict:
        self.__cursor.execute(f'SELECT * FROM {self.__collection} WHERE key = ?', (str(key),))
        return self.__extract_object(self.__cursor.fetchone())

    async def put_object(self, key: uuid, value: dict):
        await self.delete_object(key)

        original = value.get('original', str())
        translation = value.get('translation', str())
        transcription = value.get('transcription', str())

        self.__cursor.execute(
            f'INSERT INTO {self.__collection} VALUES (?, ?, ?, ?)', (str(key), original, translation, transcription,)
        )

        self.__connection.commit()

    async def delete_object(self, key: uuid):
        self.__cursor.execute(f'DELETE FROM {self.__collection} WHERE key = ?', (str(key),))
        self.__connection.commit()

    @staticmethod
    def __extract_object(row):
        return {
            'key': row[0],
            'original': row[1],
            'translation': row[2],
            'transcription': row[3],
        } if row else None
