from types import SimpleNamespace
from asyncio import sleep
from itertools import count

from starlette.routing import Mount, Route, WebSocketRoute
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.applications import Starlette


class Test(SimpleNamespace):
    async def simple(request):
        return JSONResponse({'success': True})

class WsTest(SimpleNamespace):
    async def simple(socket):
        await socket.accept()
        await socket.send_json({'success': True})
        await socket.close()

    async def counter(socket):
        await socket.accept()
        for x in count(1):
            await socket.send_json({'count': x})
            await sleep(.5)
        await socket.close()

GAMES = {
    'abc123': [],
}
class Game(SimpleNamespace):
    async def new_game(request):
        pass
    async def discard(request):
        pass
    async def build(request):
        pass
    async def capture(request):
        pass
    async def state(request):
        pass
    async def ws_state(socket):
        pass

v1_routes = [
    Route('/new/{game}/{player}',          Game.new_game),
    Route('/discard/{game}/{player}',      Game.discard),
    Route('/build/{game}/{player}',        Game.build),
    Route('/capture/{game}/{player}',      Game.capture),
    Route('/state/{game}/{player}',        Game.state),
    WebSocketRoute('/ws_state/{game}/{player}', Game.ws_state)
]

routes = [
    Mount('/v1', routes=v1_routes),
    Mount('/test', routes=[
        Route('/simple', Test.simple),
    ]),
    Mount('/wstest', routes=[
        WebSocketRoute('/simple', WsTest.simple),
        WebSocketRoute('/counter', WsTest.counter),
    ]),
]
app = Starlette(routes=routes, debug=True)
