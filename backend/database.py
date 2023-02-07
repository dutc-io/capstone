from sqlite3 import PARSE_DECLTYPES, connect

db = connect("casino.db", detect_types=PARSE_DECLTYPES, check_same_thread=False)
db.row_factory = lambda c, r: {k: v for k, v in zip([cl[0] for cl in c.description], r)}
c = db.cursor()


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


def create_game(players, state) -> int | None:
    """Save a new game"""
    
    # Create a Game
    c.execute(
        """ INSERT INTO game (players) VALUES (?) """,
        (players,),
    )
    gid = c.lastrowid
    db.commit()

    # Commit its state
    c.execute(
        """ INSERT INTO state (state, game_id) VALUES (?, ?) """,
        (state, gid),
    )
    db.commit()

    return gid

def get_game_state(gid):
    """Return most current state of a game"""
    
    # Return the current state of a game 
    c.execute(
        """ SELECT state FROM state WHERE game_id=? ORDER BY modified DESC """,
        (gid,),
    )
    # TODO: Error handling
    _state = c.fetchone()
    return _state["state"] 
