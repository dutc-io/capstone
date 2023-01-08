from saves import Saves
import json, uuid


def fake_game_round(round=1, gid='9697f0f5-2733-4a7e-98c4-6c1b8fb6d7e6'):

    return {"round": round, "gameid": gid , 
            "state": { "table": [], "deck": [], "players": [], "hands": {}, "capture": {}, "player_order": [] } }


def test_save_single():
    s = Saves(DBPath='test.db')
    s._initdb()

    gameid = str(uuid.uuid4())
    fake_game_round_1 = fake_game_round(gid=gameid)
    gameplays = [ fake_game_round_1 , ]
    s.update(gameid, gameplays)    

    g = s.get_id(gameid) 
    assert g  
    print(g['id'])
    assert g['id']==gameid 



def test_save_multiple_rounds():
    s = Saves(DBPath='test.db')
    s._initdb()

    gameid = str(uuid.uuid4())
    game_round_1 = fake_game_round(round=1,gid=gameid)
    game_round_2 = fake_game_round(round=2,gid=gameid)
    game_round_3 = fake_game_round(round=3,gid=gameid)

    # 
    gameplays = [ game_round_1 , ]
    s.update(gameid, gameplays)    

    # 
    gameplays.append(game_round_2)
    s.update(gameid, gameplays)    

    # 
    gameplays.append(game_round_3)
    s.update(gameid, gameplays)    

    all = s.get_all()
    assert len(all) == 1

    g = s.get_id(gameid) 
    assert g['id']==gameid 

    print(len(json.loads(g['data'])))
    assert len(json.loads(g['data'])) == 3


def test_save_multiple_games():
    s = Saves(DBPath='test.db')
    s._initdb()

    # 
    gameid = str(uuid.uuid4())
    game1 = fake_game_round(gid=gameid)
    gameplays = [ game1 , ]
    s.update(gameid, gameplays)    

    # 
    gameid = str(uuid.uuid4())
    game2 = fake_game_round(gid=gameid)
    gameplays = [ game2 , ]
    s.update(gameid, gameplays)    

    all = s.get_all()
    assert len(all) == 2

