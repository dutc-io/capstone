from collections import deque
from typing import List
from pytest import raises

from engine import Card, Player, Rank, State, Suit, Unit, STANDARD_DECK

DECK = [c for c in STANDARD_DECK]

state_serialized = {
    "deck": [
        {"rank": "Two", "suit": "Diamond"},
        {"rank": "Two", "suit": "Club"},
        {"rank": "Two", "suit": "Heart"},
        {"rank": "Two", "suit": "Spade"},
        {"rank": "Three", "suit": "Diamond"},
        {"rank": "Three", "suit": "Club"},
        {"rank": "Three", "suit": "Heart"},
        {"rank": "Three", "suit": "Spade"},
        {"rank": "Four", "suit": "Diamond"},
        {"rank": "Four", "suit": "Club"},
        {"rank": "Four", "suit": "Heart"},
        {"rank": "Four", "suit": "Spade"},
        {"rank": "Five", "suit": "Diamond"},
        {"rank": "Five", "suit": "Club"},
        {"rank": "Five", "suit": "Heart"},
        {"rank": "Five", "suit": "Spade"},
        {"rank": "Six", "suit": "Diamond"},
        {"rank": "Six", "suit": "Club"},
        {"rank": "Six", "suit": "Heart"},
        {"rank": "Six", "suit": "Spade"},
        {"rank": "Seven", "suit": "Diamond"},
        {"rank": "Seven", "suit": "Club"},
        {"rank": "Seven", "suit": "Heart"},
        {"rank": "Seven", "suit": "Spade"},
        {"rank": "Eight", "suit": "Diamond"},
        {"rank": "Eight", "suit": "Club"},
        {"rank": "Eight", "suit": "Heart"},
        {"rank": "Eight", "suit": "Spade"},
        {"rank": "Nine", "suit": "Diamond"},
        {"rank": "Nine", "suit": "Club"},
        {"rank": "Nine", "suit": "Heart"},
        {"rank": "Nine", "suit": "Spade"},
        {"rank": "Ten", "suit": "Diamond"},
        {"rank": "Ten", "suit": "Club"},
        {"rank": "Ten", "suit": "Heart"},
        {"rank": "Ten", "suit": "Spade"},
        {"rank": "Jack", "suit": "Diamond"},
        {"rank": "Jack", "suit": "Club"},
        {"rank": "Jack", "suit": "Heart"},
        {"rank": "Jack", "suit": "Spade"},
    ],
    "table": [
        {"cards": [{"rank": "Queen", "suit": "Spade"}], "value": 10},
        {"cards": [{"rank": "Queen", "suit": "Heart"}], "value": 10},
        {"cards": [{"rank": "Queen", "suit": "Club"}], "value": 10},
        {"cards": [{"rank": "Queen", "suit": "Diamond"}], "value": 10},
    ],
    "players": [{"name": "Hyacinth", "points": 0}, {"name": "Onslow", "points": 0}],
    "player_order": [
        {"name": "Hyacinth", "points": 0},
        {"name": "Onslow", "points": 0},
    ],
    "hands": {
        "Hyacinth": [
            {"rank": "Ace", "suit": "Spade"},
            {"rank": "Ace", "suit": "Heart"},
            {"rank": "Ace", "suit": "Club"},
            {"rank": "Ace", "suit": "Diamond"},
        ],
        "Onslow": [
            {"rank": "King", "suit": "Spade"},
            {"rank": "King", "suit": "Heart"},
            {"rank": "King", "suit": "Club"},
            {"rank": "King", "suit": "Diamond"},
        ],
    },
    "capture": {"Hyacinth": [], "Onslow": []},
}


def test_card_serialization():

    card = Card(suit=Suit.Spade, rank=Rank.Ace)
    serilaized = card.dict()
    new_card = Card(**serilaized)

    assert serilaized == {"rank": "Ace", "suit": "Spade"}

    assert type(new_card) is Card
    assert new_card.rank == "Ace"
    assert new_card.suit == "Spade"

    assert card == new_card


def test_player_serialization():

    player = Player(name="Hyacinth")
    serilaized = player.dict()
    new_player = Player(**serilaized)

    assert serilaized == {"name": "Hyacinth", "points": 0}

    assert type(new_player) is Player
    assert new_player.points == 0
    assert new_player.name == "Hyacinth"


def test_unit_serialization():
    cards = [Card(suit=Suit.Spade, rank=Rank.Ace), Card(suit=Suit.Heart, rank=Rank.Ace)]
    unit = Unit.from_card(cards[0])
    serilaized = unit.dict()
    new_unit = Unit(**serilaized)

    # XXX: serialized doesn't match exactly what we expect
    assert serilaized == {
        "cards": [{"rank": "Ace", "suit": "Spade", "value": 1}],
        "value": 1,
    }
    assert unit == new_unit

    assert type(new_unit) is Unit
    assert type(new_unit.cards) is list
    assert new_unit.cards[0].rank == "Ace"
    assert new_unit.cards[0].suit == "Spade"
    assert new_unit.value == 1


def test_state_serialization():
    players = [
        Player(name="Hyacinth"),
        Player(name="Onslow"),
    ]
    state = State.from_players(DECK, players)
    serilaized = state.dict()
    new_state = State(**serilaized)

    assert serilaized == state_serialized
    assert type(new_state) is State
