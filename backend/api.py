from json import loads
from uuid import uuid4
from types import SimpleNamespace
from asyncio import sleep
from itertools import count

from starlette.routing import Mount, Route, WebSocketRoute
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.websockets import WebSocket
from starlette.applications import Starlette

from engine import Player, game

# Testing temporary storage
GAMES = {}
MAX_PLAYERS = 6


class Test(SimpleNamespace):
    async def simple(request):
        return JSONResponse({"success": True})


class WsTest(SimpleNamespace):
    async def simple(socket):
        await socket.accept()
        await socket.send_json({"success": True})
        await socket.close()

    async def counter(socket):
        await socket.accept()
        for x in count(1):
            await socket.send_json({"count": x})
            await sleep(0.5)
        await socket.close()


class Game(SimpleNamespace):
    async def new_game(request):

        requested_players = None
        try:
            body = loads(await request.json())
            requested_players = body["players"]
            players = {Player.from_name(name) for name in requested_players}

            if len(requested_players) == 0:
                return JSONResponse(
                    {"error": "Must supply players names"}, status_code=412
                )
            elif len(requested_players) >= MAX_PLAYERS:
                return JSONResponse(
                    {"error": "Too many players, must be six or less"}, status_code=412
                )
        except Exception as e:
            # Just for testing
            return JSONResponse({"error": f"{e}"}, status_code=412)

        id = uuid4().hex
        GAMES[id] = game(players)

        return JSONResponse({"game": id}, status_code=200)

    async def discard(request):
        try:
            body = loads(await request.json())

            # XXX: Need to validate all of these
            current = body["game"]
            player = body["player"]
            card = int(body["card"])

            print(f"{current!r} {player!r} {card!r}")
            
            state = GAMES[current] 
            
            # HACK: for now to find the player
            pl = [p for p in state.players if p.name == player]
            if not pl:
                return JSONResponse({"error": "Could not fine {player!r}"}, status_code=412)
            selected_player = pl[0]
            
            # XXX: Should use logging
            print(f"{selected_player}")
            print(f"{state.hands[selected_player]}")
            print(f"{card}")

            c = [*state.hands[selected_player]][card]
            state = state.with_discard(selected_player, c)

            print(" ")
            print(
                f'{selected_player.name} discards {c.symbol}',
                '\n'.join(state.render()),
                sep='\n', end='\n\n',
            )

            GAMES[current] = state
        except Exception as e:
            return JSONResponse({"error": f"{e}"}, status_code=412)

        return JSONResponse({"message": "discard accepted"}, status_code=200)

    async def build(request):
        # takes a game, player, card and target
        return JSONResponse({"message": "Not Implemented"}, status_code=501)

    async def capture(request):
        # takes a game, player, card and target
        return JSONResponse({"message": "Not Implemented"}, status_code=501)

    async def state(request):
        # takes a game, player, card and target
        return JSONResponse({"message": "Not Implemented"}, status_code=501)

    async def ws_state(socket):
        return JSONResponse({"message": "Not Implemented"}, status_code=501)


v1_routes = [
    Route("/create/", Game.new_game, methods=["POST"]),
    Route("/discard/", Game.discard, methods=["POST"]),
    Route("/build/", Game.build, methods=["POST"]),
    Route("/capture/", Game.capture, methods=["POST"]),
    Route("/state/", Game.state),
    Route("/test/simple/", Test.simple),
    WebSocketRoute("/ws_state/", Game.ws_state),
]

routes = [
    Mount("/v1", routes=v1_routes),
    Mount(
        "/wstest",
        routes=[
            WebSocketRoute("/simple", WsTest.simple),
            WebSocketRoute("/counter", WsTest.counter),
        ],
    ),
]
app = Starlette(routes=routes, debug=True)
