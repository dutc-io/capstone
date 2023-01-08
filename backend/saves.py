#!/usr/bin/env python
from dataclasses import dataclass
from sqlite3 import connect
import json

@dataclass
class Saves():
#
    DBPath: str
#
    RMTABLE = 'drop table if exists games'
    MKTABLE = 'create table games (id varchar(3) primary key, data json)'
#
    GET_ALL = 'SELECT id, json_extract(data, "$") as data from games'
    GET_ID = 'SELECT id, data from games where id = ? '
#
    DELETE = 'DELETE FROM games WHERE id = ?'                      
    UPDATE = 'INSERT OR REPLACE INTO games values(?, ?) '
#

    def _dictate(self, cursor, row):
        fields = [column[0] for column in cursor.description] 
        return {key: value for key, value in zip(fields, row)}

    def _connect(self):
        conn = connect(self.DBPath)
        conn.row_factory = self._dictate
        return conn

    def _initdb(self):
        c = self._connect()
        c.execute(self.RMTABLE)
        c.execute(self.MKTABLE)
        c.close()
    
    def get_all(self):
        c = self._connect()
        games = c.execute(self.GET_ALL).fetchall()
        c.close()
        return games

    def get_id(self, uid):
        c = self._connect()
        game = c.execute(self.GET_ID, [uid]).fetchone()
        c.close()
        return game

    def update(self, uid, blob):
        c = self._connect()
        c.execute(self.UPDATE, (uid, json.dumps(blob)),)
        c.commit()
        c.close()

