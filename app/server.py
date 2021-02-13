from aiohttp import web

routes = web.RouteTableDef()


@routes.post('/')
async def handle_pokemon(request):
    data = await request.json()

    if ('id' or 'name') not in data:
        raise web.HTTPBadRequest

    p_weight = data.get('weight')
    p_name = data['name']

    if p_weight is None:
        pass
    elif p_weight > 100:
        p_name += '_the_boss'
    elif p_weight < 50:
        p_name = 'like_a_feather_' + p_name

    result = {'id': data['id'], 'name': p_name}

    return web.json_response(data=result)


app = web.Application()
app.add_routes(routes)


if __name__ == "__main__":
    web.run_app(app)
