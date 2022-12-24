#!/usr/bin/env python3
from enum import Enum
from random import Random
from typing import Union
from operator import or_
from functools import cached_property, reduce
from itertools import product
from contextlib import contextmanager
from collections import deque, namedtuple
from dataclasses import dataclass, replace


class NotTurnException(Exception):
    ...


class MissingPlayerException(Exception):
    ...


Suit = Enum(
    "Suit",
    """
    Diamond Club
    Heart Spade
""",
)
Rank = Enum(
    "Rank",
    """
    Two Three Four Five Six
    Seven Eight Nine Ten
    Jack Queen King Ace
""",
)


class Card(namedtuple("Card", "rank suit")):
    SUITS = {
        Suit.Diamond: "\N{black diamond suit}",
        Suit.Club: "\N{black club suit}",
        Suit.Heart: "\N{black heart suit}",
        Suit.Spade: "\N{black spade suit}",
    }
    RANKS = {
        Rank.Two: " 2 ",
        Rank.Three: " 3 ",
        Rank.Four: " 4 ",
        Rank.Five: " 5 ",
        Rank.Six: " 6 ",
        Rank.Seven: " 7 ",
        Rank.Eight: " 8 ",
        Rank.Nine: " 9 ",
        Rank.Ten: " 10",
        Rank.Jack: " J ",
        Rank.Queen: " Q ",
        Rank.King: " K ",
        Rank.Ace: " A ",
    }
    VALUES = {
        Rank.Ace: 1,
        Rank.Two: 2,
        Rank.Three: 3,
        Rank.Four: 4,
        Rank.Five: 5,
        Rank.Six: 6,
        Rank.Seven: 7,
        Rank.Eight: 8,
        Rank.Nine: 9,
        Rank.Ten: 10,
    }

    @cached_property
    def value(self):
        return self.VALUES.get(self.rank)

    @cached_property
    def symbol(self):
        if self.suit in {Suit.Heart, Suit.Diamond}:
            return (
                f"\033[1;41m{self.RANKS[self.rank]}{self.SUITS[self.suit]} \033[1;37;0m"
            )
        return f"\033[1;7m{self.RANKS[self.rank]}{self.SUITS[self.suit]} \033[1;37;0m"


STANDARD_DECK = [Card(r, s) for r, s in product(Rank, Suit)]

# trail: discard
# combine: build
# pair: capture


@dataclass(frozen=True)
class Player:
    name: str
    points: int = 0

    @classmethod
    def from_name(cls, name):
        return cls(name=name)

    def __hash__(self):
        return hash(self.name)


@dataclass(frozen=True)
class Unit:
    cards: frozenset[Card]
    value: Union[int, None] = None

    @classmethod
    def from_card(cls, card):
        return cls(cards=frozenset({card}), value=card.value)

    def render(self):
        if len(self.cards):
            return "【{}】".format(" ".join(c.symbol.lstrip() for c in self.cards))
        return " ".join(c.symbol for c in self.cards)

    def __or__(self, other):
        if self.value is None or other.value is None:
            raise ValueError("cannot combine")
        if (self.value + other.value) > max(Card.VALUES.values()):
            raise ValueError("cannot combine")
        return Unit(
            cards=frozenset({*self.cards, *other.cards}), value=self.value + other.value
        )

    def __hash__(self):
        return hash(self.cards)


@dataclass(frozen=True)
class State:
    deck: deque[Card]
    table: frozenset[Unit]
    players: frozenset[Player]
    hands: dict[Player, frozenset[Card]]
    capture: dict[Player, frozenset[Card]]
    player_order: deque[Player]

    @contextmanager
    def players_turn(self, player_name):
        _player = None
        for p in self.players:
            if p.name == player_name:
                _player = p
                break

        if not _player:
            raise MissingPlayerException(f"Could not find player {player_name!r}")

        if _player is not self.player_order[0]:
            raise NotTurnException(f"Not {player_name!r}'s turn")

        player = self.player_order.popleft()
        try:
            yield player
        finally:
            self.player_order.append(player)

    @classmethod
    def from_players(cls, deck, *players):
        return cls(
            deck=deck,
            table=frozenset(),
            players=frozenset(players),
            hands={pl: frozenset() for pl in players},
            capture={pl: frozenset() for pl in players},
            player_order=deque(players),
        )

    def with_deal(self):
        deck = [*self.deck]
        table = {*self.table}
        hands = {pl: {*h} for pl, h in self.hands.items()}
        for _ in range(2):
            for h in hands.values():
                h.update(deck.pop() for _ in range(2))
            table.update(Unit.from_card(deck.pop()) for _ in range(2))
        return replace(
            self,
            deck=deck,
            table=frozenset(table),
            hands={k: frozenset(v) for k, v in hands.items()},
        )

    def with_discard(self, player, card):
        deck = [*self.deck]
        table = {*self.table}
        hand = {*self.hands[player]}

        hand.remove(card)
        table.add(Unit.from_card(card))
        hand.add(deck.pop())

        return replace(
            self,
            deck=deck,
            table=frozenset(table),
            hands={**self.hands, player: frozenset(hand)},
        )

    def with_build(self, player, card, *targets):
        deck = [*self.deck]
        table = {*self.table}
        hand = {*self.hands[player]}

        hand.remove(card)
        table.difference_update(targets)
        table.add(reduce(or_, {*targets, Unit.from_card(card)}))
        hand.add(deck.pop())

        return replace(
            self,
            deck=deck,
            table=frozenset(table),
            hands={**self.hands, player: frozenset(hand)},
        )

    def with_capture(self, player, card, *targets):
        deck = [*self.deck]
        table = {*self.table}
        hand = {*self.hands[player]}

        if not all(card.value == t.value for t in targets):
            raise ValueError(f"cannot capture {targets} with {card}")

        hand.remove(card)
        table.difference_update(targets)
        hand.add(deck.pop())

        return replace(
            self,
            deck=deck,
            table=frozenset(table),
            hands={**self.hands, player: frozenset(hand)},
        )

    def render(self):
        return (
            "",
            f"Current Turn: {self.player_order[0].name}",
            f"Table: {' '.join(u.render() for u in self.table)}\n",
            *(
                f"{p.name:<8} {'  '.join(c.symbol for c in h)}"
                for p, h in sorted(self.hands.items(), key=lambda pl_h: pl_h[0].name)
            ),
        )


def game(players, seed=0, _deck=None):
    rnd = Random(seed)
    if _deck:
        deck = _deck
    else:
        deck = [c for c in STANDARD_DECK]
        rnd.shuffle(deck)
    state = State.from_players(deck, *players)
    state = state.with_deal()

    return state


if __name__ == "__main__":

    DECK = [c for c in STANDARD_DECK]
    deck = [d for d in DECK if d.rank.value in [2, 3, 5]]
    print(f" ".join([c.symbol for c in deck]))
