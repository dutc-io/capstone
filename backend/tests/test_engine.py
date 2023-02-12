from collections import deque
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
    print(card)

    assert type(card) is Card
    assert card.rank == Rank.Ace
    assert card.suit == Suit.Spade


def test_unit():

    cards = [Card(suit=Suit.Spade, rank=Rank.Ace), Card(suit=Suit.Heart, rank=Rank.Ace)]
    unit = Unit(cards=frozenset(cards), value=None)
    u = Unit.from_card(cards[0])

    assert type(u) is Unit
    assert u.value == 1
    assert type(unit) is Unit
    assert unit.value == None 


def test_state():

    name = "Hyacinth"

    player = Player(name=name)
    card = Card(suit=Suit.Spade, rank=Rank.Ace)
    deck = deque([card])
    unit = Unit.from_card(card)
    table = frozenset([unit])
    players = frozenset([player])
    hands = {player: frozenset([card])}
    capture = {player: frozenset([card])}
    player_order = deque([player])

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
    state = State.from_players(DECK, *players)

    assert type(state) is State
