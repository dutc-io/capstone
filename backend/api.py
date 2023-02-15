from logging import getLogger

from starlette.requests import Request

# from starlette.responses import JSONResponse

from fastapi import FastAPI, Response

from engine import game, Player, State
from database import (
    create_game,
    CreateNewGameRequest,
    get_game_state,
    init_db,
    insert_game_state,
    NewGameResponse,
)

logger = getLogger("uvicorn")

app = FastAPI(
    on_startup=[init_db],
    on_shutdown=[],  # Lets keep the db for now?
)


@app.get("/", description="Proof of life")
def index():
    """POL"""
    return {"ping": "pong"}


@app.post("/v1/game/create", response_model=NewGameResponse)
async def game_create(request: Request, cgr: CreateNewGameRequest, response: Response):
    # XXX: Hack CORS for now.
    response.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]

    players = [Player(name=p) for p in cgr.players]
    if not (game_id := create_game(players)):
        return NewGameResponse(
            players=cgr.players, game_id=None, error="Unable to create game"
        )

    # # XXX: Just mock for now. Create a new game
    state = game(players)
    insert_game_state(game_id, state.dict())

    return NewGameResponse(players=cgr.players, game_id=game_id)


@app.post(
    "/v1/game/action",
    description="Preform an action within a game. Valid actions are `discard`, `build`, `capture`",
)
def game_action():
    return {"action": "build, capture, discard"}


@app.get(
    "/v1/game/{game_id}/state/",
    description="Return the state of a game",
    response_model=State,
)
async def game_state(game_id: int):
    gs = get_game_state(game_id)
    state = State(**gs)
    return state
