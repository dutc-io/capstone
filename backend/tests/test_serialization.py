from os import wait
from pytest import raises
from json import dumps

from engine import (
    Card,
    game,
    MissingPlayerException,
    Player,
    Rank,
    STANDARD_DECK,
    Suit,
    Unit,
    State,
)

# Smoke tests (that basically test that pytest is working). But maybe a
# starting porint?

# python hashseed set to 0 via export PYTHONHASHSEED=0

DECK = [c for c in STANDARD_DECK]


def test_players_to_json():

    player_to_create = "Hyacinth"
    player = Player.from_name(player_to_create)
    serialized = player.to_json()

    assert serialized == dumps({"name": "Hyacinth", "points": 0})


def test_players_from_json():

    serialized = dumps({"name": "Hyacinth", "points": 0})
    player = Player.from_json(serialized)

    assert player.name == "Hyacinth"
    assert player.points == 0
    assert type(player) == Player


def test_card_to_json():

    queen_of_heards = Card(rank=Rank.Queen, suit=Suit.Heart)
    serialized = queen_of_heards.to_json()

    assert serialized == dumps({"rank": 11, "suit": 3})


def test_card_from_json():

    serialized = dumps({"rank": 11, "suit": 3})
    queen_of_heards = Card.from_json(serialized)

    assert type(queen_of_heards) == Card
    assert queen_of_heards.rank == Rank.Queen
    assert queen_of_heards.suit == Suit.Heart


def test_unit_to_json():

    queen_of_heards = Card(rank="Queen", suit="Heart")
    unit = Unit(cards=frozenset(queen_of_heards), value=1)

    serialized = unit.to_json()
    print(serialized)
    # assert serialized == dumps(
    #     {"cards": [{"rank": "Queen", "suit": "Heart"}], "value": 1}
    # )

def test_unit_from_json():

    # queen_of_heards = Card(rank="Queen", suit="Heart")
    # _unit = Unit(cards=frozenset(queen_of_heards), value=1)
    # print(_unit.to_json())

    djson = dumps({"cards": [{"rank": "Queen", "suit": "Heart"}], "value": 1})

    unit = Unit.from_json(djson)
    # assert type(unit) == Unit 
    print(unit)

def test_state_to_json():
    state_json = '{"deck": ["{\\"rank\\": 2, \\"suit\\": 1}", "{\\"rank\\": 2, \\"suit\\": 2}", "{\\"rank\\": 2, \\"suit\\": 3}", "{\\"rank\\": 2, \\"suit\\": 4}", "{\\"rank\\": 3, \\"suit\\": 1}", "{\\"rank\\": 3, \\"suit\\": 2}", "{\\"rank\\": 3, \\"suit\\": 3}", "{\\"rank\\": 3, \\"suit\\": 4}", "{\\"rank\\": 5, \\"suit\\": 1}", "{\\"rank\\": 5, \\"suit\\": 2}", "{\\"rank\\": 5, \\"suit\\": 3}", "{\\"rank\\": 5, \\"suit\\": 4}"], "table": [], "players": ["{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}"], "hands": {"{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}": []}, "capture": {"{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}": []}, "player_order": ["{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}"]}'

    DECK = [c for c in STANDARD_DECK]
    deck = [d for d in DECK if d.rank.value in [2, 3, 5]]
    player_to_create = "Hyacinth"
    player = Player.from_name(player_to_create)
    state = State.from_players(deck, *[player])

    serialized = state.to_json()

    assert serialized == state_json


def test_state_from_json():
    state_json = '{"deck": ["{\\"rank\\": 2, \\"suit\\": 1}", "{\\"rank\\": 2, \\"suit\\": 2}", "{\\"rank\\": 2, \\"suit\\": 3}", "{\\"rank\\": 2, \\"suit\\": 4}", "{\\"rank\\": 3, \\"suit\\": 1}", "{\\"rank\\": 3, \\"suit\\": 2}", "{\\"rank\\": 3, \\"suit\\": 3}", "{\\"rank\\": 3, \\"suit\\": 4}", "{\\"rank\\": 5, \\"suit\\": 1}", "{\\"rank\\": 5, \\"suit\\": 2}", "{\\"rank\\": 5, \\"suit\\": 3}", "{\\"rank\\": 5, \\"suit\\": 4}"], "table": [], "players": ["{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}"], "hands": {"{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}": []}, "capture": {"{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}": []}, "player_order": ["{\\"name\\": \\"Hyacinth\\", \\"points\\": 0}"]}'

    DECK = [c for c in STANDARD_DECK]
    deck = [d for d in DECK if d.rank.value in [2, 3, 5]]
    player_to_create = "Hyacinth"
    player = Player.from_name(player_to_create)
    state = State.from_players(deck, *[player])

    state_from_json = State.from_json(state_json)

    print(state)
    print(" ")
    print(state_from_json)
    print(" ")

    assert type(state_from_json) == State
    assert state_from_json.deck[0] == Card(rank=Rank.Three, suit=Suit.Diamond)
