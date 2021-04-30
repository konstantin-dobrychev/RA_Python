import uuid

from pathlib import Path
from typing import AsyncIterable

from aiohttp import web
from aiohttp_swagger import *

import aiohttp_jinja2
import jinja2

from CollectionManager import CollectionManager
from DataStorage import DataStorage


routes = web.RouteTableDef()


async def __get_collection_storage(request: web.Request, name: str) -> DataStorage:
    manager: CollectionManager = request.app['collection_manager']
    return await manager.data_storage(name)


async def __to_list(iterable: AsyncIterable) -> list:
    return [item async for item in iterable]


@routes.get('/')
async def root(_request: web.Request) -> web.Response:
    raise web.HTTPFound(location='/collections')


@routes.get('/collections')
@aiohttp_jinja2.template('collections.jinja2')
async def collections(request: web.Request) -> dict:
    manager: CollectionManager = request.app['collection_manager']
    return {'collections': manager.collections()}


@routes.get('/collections/{collection}')
@aiohttp_jinja2.template('collection.jinja2')
async def collection(request: web.Request) -> dict:
    name = request.match_info['collection']
    storage: DataStorage = await __get_collection_storage(request, name)

    return {'name': name, 'collection': await __to_list(storage.get_objects())}


@routes.post('/collections/{collection}')
async def add_object(request: web.Request) -> web.Response:
    data = await request.post()

    name = request.match_info['collection']
    storage: DataStorage = await __get_collection_storage(request, name)

    await storage.put_object(uuid.uuid4(), {
        'original': data['original'],
        'translation': data['translation'],
        'transcription': data['transcription'],
    })

    return web.HTTPFound(location=f'/collections/{name}')


@routes.get('/api/collections', allow_head=False)
async def collections(request: web.Request) -> web.Response:
    """
    description: Получить список коллекций слов.
    tags:
    - Collections
    produces:
    - application/json
    responses:
        "200":
            description: возвращает список коллекций
    """

    manager: CollectionManager = request.app['collection_manager']
    return web.json_response(manager.collections())


@swagger_path('docs/collection.yml')
@routes.get('/api/collections/{collection}', allow_head=False)
async def collection(request: web.Request) -> web.Response:
    manager: CollectionManager = request.app['collection_manager']
    storage: DataStorage = await manager.data_storage(request.match_info['collection'])

    return web.json_response(await __to_list(storage.get_objects()))


@swagger_path('docs/get_object.yml')
@routes.get('/api/collections/{collection}/{key}', allow_head=False)
async def get_object(request: web.Request) -> web.Response:
    key = request.match_info['key']
    storage: DataStorage = await __get_collection_storage(request, request.match_info['collection'])

    return web.json_response(await storage.get_object(request.match_info['key'])) \
        if await storage.contains(key) else web.HTTPNotFound()


@swagger_path('docs/add_object.yml')
@routes.post('/api/collections/{collection}')
async def add_object(request: web.Request) -> web.Response:
    data = await request.json()

    storage: DataStorage = await __get_collection_storage(request, request.match_info['collection'])
    await storage.put_object(uuid.uuid4(), data)

    return web.HTTPCreated()


@swagger_path('docs/update_object.yml')
@routes.put('/api/collections/{collection}/{key}')
async def update_object(request: web.Request) -> web.Response:
    key = request.match_info['key']
    storage: DataStorage = await __get_collection_storage(request, request.match_info['collection'])

    if await storage.contains(key):
        data = await request.json()
        await storage.put_object(key, data)

        return web.HTTPNoContent()
    else:
        return web.HTTPNotFound()


@swagger_path('docs/delete_object.yml')
@routes.delete('/api/collections/{collection}/{key}')
async def delete_object(request: web.Request) -> web.Response:
    key = request.match_info['key']
    storage: DataStorage = await __get_collection_storage(request, request.match_info['collection'])

    if await storage.contains(key):
        await storage.delete_object(key)
        return web.HTTPNoContent()
    else:
        return web.HTTPNotFound()


if __name__ == '__main__':
    settings = {
        'port': 8080,
        'data_storage': {
            'storage': 'mongo',
            'database': 'testdb',
        }
    }

    collections = [
        'animals',
        'furniture',
    ]

    templates_directory = Path(__file__).parent.joinpath('templates')

    app = web.Application()
    app['collection_manager'] = CollectionManager(collections, settings['data_storage'])

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates_directory)))
    app.add_routes(routes)

    setup_swagger(app, title='Words reminder API')

    web.run_app(app, host='localhost', port=settings['port'])
