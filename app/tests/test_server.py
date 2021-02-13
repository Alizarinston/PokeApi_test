import json

import pytest
from aiohttp import web

from app.server import handle_pokemon


@pytest.fixture
def cli(loop, aiohttp_client):
    app = web.Application()
    app.router.add_post('/', handle_pokemon)
    return loop.run_until_complete(aiohttp_client(app))


@pytest.mark.parametrize("weight", [10, 70, 110])
async def test_positive(cli, weight):
    data = {
        'id': 1,
        'name': 'test',
        'weight': weight,
        'payload': None
    }

    resp = await cli.post('/', data=json.dumps(data))
    assert resp.status == 200

    expected = {
        'id': data['id'],
        'name': data['name']
    }

    if data['weight'] > 100:
        expected['name'] = data['name'] + '_the_boss'
    elif data['weight'] < 50:
        expected['name'] = 'like_a_feather_' + data['name']

    assert await resp.json() == expected


async def test_negative(cli):

    data = {
        'name': 'test',
        'payload': None
    }

    resp = await cli.post('/', data=json.dumps(data))
    assert resp.status == 400
    assert resp.reason == 'Bad Request'
