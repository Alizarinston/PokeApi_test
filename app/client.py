import asyncio
import aiohttp
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('client')


async def get_common_session():
    return aiohttp.ClientSession()


async def send_filtered_pokemon(url, server_session):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            pokemon = await response.json()

            p_types = pokemon['types']
            if len(p_types) > 1 and ("fire" or "grass" in [elem['type']['name'] for elem in p_types]):
                response = await server_session.post('http://localhost:8080/', json=pokemon)

                logger.info(await response.json())


if __name__ == "__main__":
    pokemons = requests.get('https://pokeapi.co/api/v2/pokemon?limit=50').json()

    loop = asyncio.get_event_loop()
    common_session = loop.run_until_complete(get_common_session())

    test = loop.run_until_complete(
        asyncio.gather(*[send_filtered_pokemon(pokemon['url'], common_session) for pokemon in pokemons['results']])
    )

    loop.run_until_complete(common_session.close())
