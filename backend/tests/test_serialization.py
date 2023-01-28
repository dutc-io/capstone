from pytest import raises

from engine import game, MissingPlayerException, Player, STANDARD_DECK, Suit, Rank

# Smoke tests (that basically test that pytest is working). But maybe a
# starting porint?

# python hashseed set to 0 via export PYTHONHASHSEED=0

DECK = [c for c in STANDARD_DECK]

def test_players_to_dict():

    player_to_create = "Hyacinth"
    player = Player.from_name(player_to_create)
    
    serialized = player.to_json()

    assert serialized == {"name": "Hyacinth", "points": 0} 

def test_players_from_json():

    serialized = {"name": "Hyacinth", "points": 0}
    player = Player.from_json(serialized)

    assert player.name == "Hyacinth"  
    assert player.points == 0 
    assert type(player) == Player 
