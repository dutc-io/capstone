from collections import deque
from typing import List
from pytest import raises

from engine import Card, Player, Rank, State, Suit, Unit, STANDARD_DECK

# Smoke tests (that basically test that pytest is working). But maybe a
# starting porint?

# python hashseed set to 0 via export PYTHONHASHSEED=0

DECK = [c for c in STANDARD_DECK]


def test_suits():

    suits = ["Diamond", "Club", "Heart", "Spade"]

    for s in suits:
        assert Suit[s]

    assert len([*Suit]) == len(suits)


def test_rank():

    ranks = [
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]

    for r in ranks:
        assert Rank[r]

    assert len([*Rank]) == len(ranks)


def test_player_create():

    name = "Hyacinth"
    player = Player(name=name)

    assert type(player) is Player
    assert player.points == 0
    assert player.name == name


def test_cards():

    card = Card(suit=Suit.Spade, rank=Rank.Ace)

    assert type(card) is Card
    assert card.rank == "Ace"
    assert card.suit == "Spade"


def test_unit():

    cards = [Card(suit=Suit.Spade, rank=Rank.Ace), Card(suit=Suit.Heart, rank=Rank.Ace)]
    unit = Unit(cards=cards, value=None)
    u = Unit.from_card(cards[0])

    assert type(u) is Unit
    assert u.value == 1
    assert type(unit) is Unit
    assert type(unit.cards) is list
    assert unit.value == None


def test_state():

    player = Player(name="Hyacinth")
    card = Card(suit=Suit.Spade, rank=Rank.Ace)
    deck = [card]
    unit = Unit.from_card(card)
    table = [unit]
    players = [player]
    hands = {player.name: [card]}
    capture = {player.name: [card]}
    player_order = [player]

    state = State(
        deck=deck,
        table=table,
        players=players,
        hands=hands,
        capture=capture,
        player_order=player_order,
    )

    assert type(state) is State


def test_state_from_players():

    players = [
        Player(name="Hyacinth"),
        Player(name="Rose"),
        Player(name="Daisy"),
        Player(name="Onslow"),
    ]
    state = State.from_players(DECK, players)

    assert type(state) is State

def test_state_from_players_named_the_same():
    
    # XXX: Currently this failes, and is one of the downfalls of using a `str`
    # key name and not the actual player class.
    players = [
        Player(name="Hyacinth"),
        Player(name="Hyacinth"),
    ]
    state = State.from_players(DECK, players)
    assert len(state.hands.keys()) == 2
