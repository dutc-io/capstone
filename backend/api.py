from json import loads, dumps
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
import database

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
            if len(requested_players) == 0:
                return JSONResponse(
                    {"error": "Must supply players names"}, status_code=412
                )
            elif len(requested_players) >= MAX_PLAYERS:
                return JSONResponse(
                    {"error": "Too many players, must be six or less"}, status_code=412
                )
            players = {Player.from_name(name) for name in requested_players}
        except Exception as e:
            return JSONResponse({"error": f"{e}"}, status_code=412)
        
        # XXX: This seems a bit verbose.
        id = uuid4().hex
        state = game(players)
        GAMES[id] = state

        print(
            '\n'.join(state.render()),
            sep='\n', end='\n\n',
        )

        return JSONResponse({"game": id}, status_code=200)

    async def discard(request):
        try:
            body = loads(await request.json())
            
            # Make sure a gamge exists
            current = body["game"]
            if current not in GAMES:
                return JSONResponse({"error": f"Unable to find game {current!r}"}, status_code=412)
            state = GAMES[current] 
            
            with state.players_turn(body["player"]) as player:
                try:
                    card = [*state.hands[player]][body["card"]]
                except IndexError:
                    return JSONResponse({"error": f"Unable to find card {body['card']}"}, status_code=412)
                except Exception as e:
                    return JSONResponse({"error": f"{e}"}, status_code=412)

                try:
                    state = state.with_discard(player, card)
                except ValueError:
                    return JSONResponse({"Rejected": f"Unable to discard {player!r} {card!r}"}, status_code=412)

                print(" ")
                print(
                    f'{player.name} discards {card.symbol}',
                    '\n'.join(state.render()),
                    sep='\n', end='\n\n',
                )

                GAMES[current] = state
        except Exception as e:
            return JSONResponse({"error": f"{e}"}, status_code=412)
        
        return JSONResponse({"message": "discard accepted"}, status_code=200)

    async def build(request):
        try:
            body = loads(await request.json())
            
            # Make sure a gamge exists
            current = body["game"]
            if current not in GAMES:
                return JSONResponse({"error": f"Unable to find game {current!r}"}, status_code=412)
            state = GAMES[current] 

            with state.players_turn(body["player"]) as player:
                try:
                    card = [*state.hands[player]][body["card"]]
                except IndexError:
                    return JSONResponse({"error": f"Unable to find card {body['card']}"}, status_code=412)
                except Exception as e:
                    return JSONResponse({"error": f"{e}"}, status_code=412)

                try:
                    target = [*state.table][body["target"]]
                except IndexError:
                    return JSONResponse({"error": f"Unable to find card {body['target']}"}, status_code=412)
                except Exception as e:
                    return JSONResponse({"error": f"{e}"}, status_code=412)
                
                try:
                    state = state.with_build(player, card, target)
                except ValueError:
                    return JSONResponse({"Rejected": f"Unable to build {player!r} {card!r} {target!r}"}, status_code=412)

                print(" ")
                print(
                    f'{player.name} builds {target}',
                    '\n'.join(state.render()),
                    sep='\n', end='\n\n',
                )

                GAMES[current] = state
        except Exception as e:
            return JSONResponse({"error": f"{e}"}, status_code=412)
        
        return JSONResponse({"message": "build accepted"}, status_code=200)

    async def capture(request):
        try:
            body = loads(await request.json())
            
            # Make sure a gamge exists
            current = body["game"]
            if current not in GAMES:
                return JSONResponse({"error": f"Unable to find game {current!r}"}, status_code=412)
            state = GAMES[current] 

            with state.players_turn(body["player"]) as player:
                try:
                    card = [*state.hands[player]][body["card"]]
                except IndexError:
                    return JSONResponse({"error": f"Unable to find card {body['card']}"}, status_code=412)
                except Exception as e:
                    return JSONResponse({"error": f"{e}"}, status_code=412)

                try:
                    target = [*state.table][body["target"]]
                except IndexError:
                    return JSONResponse({"error": f"Unable to find card {body['target']}"}, status_code=412)
                except Exception as e:
                    return JSONResponse({"error": f"{e}"}, status_code=412)
                
                try:
                    state = state.with_capture(player, card, target)
                except ValueError:
                    return JSONResponse({"Rejected": f"Unable to capture {player!r} {card!r} {target!r}"}, status_code=412)

                print(" ")
                print(
                    f'{player.name} captures {target}',
                    '\n'.join(state.render()),
                    sep='\n', end='\n\n',
                )

                GAMES[current] = state
        except Exception as e:
            return JSONResponse({"error": f"{e}"}, status_code=412)
        
        return JSONResponse({"message": "capture accepted"}, status_code=200)

    async def save(request):

        try:
            body = loads(await request.json())

            current = body["game"]
            if current not in GAMES:
                return JSONResponse({"error": f"Unable to find game {current!r}"}, status_code=412)

            state = GAMES[current] 
            plist = [ p.name for p in state.player_order ] 
            table = [ [ c.symbol[7:11].strip() for c in u.cards ] for u in state.table ]
            hands = { pl.name: [
                        c.symbol[7:11].strip() for c in {*h}
                        ]
                     for pl, h in state.hands.items()
                     }
            deck = [ c.symbol[7:11].strip() for c in state.deck ]
            points = { p.name: p.points for p in state.players }

            mock_encoded = { 
                'gameid': current, 
                'round': 0,
                'players': plist,
                'completed': False,
                'state': {
                    'player_order': plist,
                    'table': table,
                    'deck': deck,
                    'hands': hands,
                    'points': points, 
                    }, 
                }
            database.update(current, mock_encoded)
        except Exception as e:
            return JSONResponse({"error": f"{e}"}, status_code=412)
        #
        return JSONResponse({"message": dumps(mock_encoded)}, status_code=200)

    async def state(request):
        # TODO: Need to write an StateEncoder?
        return JSONResponse({"message": "Not Implemented"}, status_code=501)

    async def ws_state(socket):
        return JSONResponse({"message": "Not Implemented"}, status_code=501)


v1_routes = [
    Route("/create/", Game.new_game, methods=["POST"]),
    Route("/discard/", Game.discard, methods=["POST"]),
    Route("/build/", Game.build, methods=["POST"]),
    Route("/capture/", Game.capture, methods=["POST"]),
    Route("/state/", Game.state),
    Route("/save/", Game.save, methods=["POST"]),
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

app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[database.create_tables],
    on_shutdown=[],
)
