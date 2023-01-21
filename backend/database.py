#
from sqlite3 import PARSE_DECLTYPES, connect

db = connect('casino.db', detect_types=PARSE_DECLTYPES, check_same_thread=False)
db.row_factory = lambda c, r: {k: v for k, v in zip([cl[0] for cl in c.description], r)} 
c = db.cursor()


def get_id(uid):
    game = c.execute(
              'SELECT * FROM game where name=(?) order by modified'
              , [uid]
              ).fetchone()
    return game


def update(uid, blob):
    INSERT_GAME = f'INSERT OR REPLACE into game(name) values("{uid}");'

    INSERT_ROUND = ( 
        f'INSERT INTO round(game_id, state) values('
        f'(select id from game where name="{uid}"), "{blob}");'
                   )
    # print(INSERT_GAME)
    c.execute(INSERT_GAME)
    # print(INSERT_ROUND)
    c.execute(INSERT_ROUND)
    db.commit()

#

def create_tables():
    #
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS game (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created     DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified    DATETIME DEFAULT CURRENT_TIMESTAMP,
            name        TEXT NOT NULL
        );
        '''
    )
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS round (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            created     DATETIME DEFAULT CURRENT_TIMESTAMP,
            modified    DATETIME DEFAULT CURRENT_TIMESTAMP,
            game_id     INTEGER,
            state       JSON,
             
            FOREIGN KEY (game_id) REFERENCES game(id)
        );
        '''
    )
    c.execute("CREATE INDEX IF NOT EXISTS game_idx ON round(game_id)")


