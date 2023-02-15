from typing import List
from json import dumps, loads
from sqlite3 import connect, PARSE_DECLTYPES

from pydantic import BaseModel
from engine import Player

db = connect("casino.db", detect_types=PARSE_DECLTYPES, check_same_thread=False)
db.row_factory = lambda c, r: {k: v for k, v in zip([cl[0] for cl in c.description], r)}
c = db.cursor()

class CreateNewGameRequest(BaseModel):
    # Need to validate its not empty 
    players: List[str] 

class NewGameResponse(BaseModel):
    players: List[str] 
    game_id: int | None
    error: str | None = None

def init_db():
    """Initialize Database"""
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS game (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created     DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified    DATETIME DEFAULT CURRENT_TIMESTAMP,
            name        TEXT,
            players     JSON
        );
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS state (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created     DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified    DATETIME DEFAULT CURRENT_TIMESTAMP,
            game_id     INTEGER,
            state       JSON,
             
            FOREIGN KEY (game_id) REFERENCES game(id)
        );
        """
    )


def create_game(players: List[Player]) -> int | None:
    """Save a new game"""
    
    # Create a Game
    c.execute(
        """ INSERT INTO game (players) VALUES (?) """,
        # There has to be a better way then `dumps`
        (dumps({"players": [p.dict() for p in players]}),),
    )
    gid = c.lastrowid

    return gid

def insert_game_state(game_id, state):
    """Add a state to a game"""

    c.execute(
        """ INSERT INTO state (state, game_id) VALUES (?, ?) """,
        (dumps(state), game_id),
    )
    db.commit()

def get_game_state(gid):
    """Return most current state of a game"""
    
    # Return the current state of a game 
    c.execute(
        """ SELECT state FROM state WHERE game_id=? ORDER BY modified DESC """,
        (gid,),
    )

    # TODO: Error handling
    _state = c.fetchone()
    return loads(_state['state'])

