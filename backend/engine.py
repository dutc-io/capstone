#!/usr/bin/env python3

from collections import deque
from random import Random
from enum import Enum
from itertools import product
from functools import cached_property, reduce
from dataclasses import dataclass, replace
from collections import namedtuple
from operator import or_
from typing import Union
from sys import exit; import sys; sys.breakpointhook = exit; del sys, exit

Suit = Enum('Suit', '''
    Diamond Club
    Heart Spade
''')
Rank = Enum('Rank', '''
    Two Three Four Five Six
    Seven Eight Nine Ten
    Jack Queen King Ace
''')

class Card(namedtuple('Card', 'rank suit')):
    SUITS = {
        Suit.Diamond:  '\N{black diamond suit}',
        Suit.Club:     '\N{black club suit}',
        Suit.Heart:    '\N{black heart suit}',
        Suit.Spade:    '\N{black spade suit}',
    }
    RANKS = {
        Rank.Two:    '2',
        Rank.Three:  '3',
        Rank.Four:   '4',
        Rank.Five:   '5',
        Rank.Six:    '6',
        Rank.Seven:  '7',
        Rank.Eight:  '8',
        Rank.Nine:   '9',
        Rank.Ten:    '10',
        Rank.Jack:   'J',
        Rank.Queen:  'Q',
        Rank.King:   'K',
        Rank.Ace:    'A',
    }
    VALUES = {
        Rank.Ace:    1,
        Rank.Two:    2,
        Rank.Three:  3,
        Rank.Four:   4,
        Rank.Five:   5,
        Rank.Six:    6,
        Rank.Seven:  7,
        Rank.Eight:  8,
        Rank.Nine:   9,
        Rank.Ten:    10,
    }

    @cached_property
    def value(self):
        return self.VALUES.get(self.rank)

    @cached_property
    def symbol(self):
        return f'{self.RANKS[self.rank]}{self.SUITS[self.suit]}'

STANDARD_DECK = [Card(r, s) for r, s in product(Rank, Suit)]

# trail: discard
# combine: build
# pair: capture

@dataclass(frozen=True)
class Player:
    name   : str
    points : int = 0
    @classmethod
    def from_name(cls, name):
        return cls(name=name)

    def __hash__(self):
        return hash(self.name)

@dataclass(frozen=True)
class Unit:
    cards : frozenset[Card]
    value : Union[int, None] = None

    @classmethod
    def from_card(cls, card):
        return cls(cards=frozenset({card}), value=card.value)

    def render(self):
        if len(self.cards):
            return '【{}】'.format(' '.join(c.symbol for c in self.cards))
        return ' '.join(c.symbol for c in self.cards)

    def __or__(self, other):
        if self.value is None or other.value is None:
            raise ValueError('cannot combine')
        if (self.value + other.value) > max(Card.VALUES.values()):
            raise ValueError('cannot combine')
        return Unit(cards=frozenset({*self.cards, *other.cards}), value=self.value+other.value)

    def __hash__(self):
        return hash(self.cards)

@dataclass(frozen=True)
class State:
    deck    : deque[Card]
    table   : frozenset[Unit]
    players : frozenset[Player]
    hands   : dict[Player, frozenset[Card]]
    capture : dict[Player, frozenset[Card]]

    @classmethod
    def from_players(cls, deck, *players):
        return cls(
            deck=deck,
            table=frozenset(),
            players=frozenset(players),
            hands={pl: frozenset() for pl in players},
            capture={pl: frozenset() for pl in players},
        )

    def with_deal(self):
        deck = [*self.deck]
        table = {*self.table}
        hands = {pl: {*h} for pl, h in self.hands.items()}
        for _ in range(2):
            for h in hands.values():
                h.update(deck.pop() for _ in range(2))
            table.update(Unit.from_card(deck.pop()) for _ in range(2))
        return replace(self, deck=deck, table=frozenset(table), hands={k: frozenset(v) for k, v in hands.items()})

    def with_discard(self, player, card):
        deck = [*self.deck]
        table = {*self.table}
        hand = {*self.hands[player]}

        hand.remove(card)
        table.add(Unit.from_card(card))
        hand.add(deck.pop())

        return replace(self, deck=deck, table=frozenset(table), hands={**self.hands, pl: frozenset(hand)})

    def with_build(self, player, card, *targets):
        deck = [*self.deck]
        table = {*self.table}
        hand = {*self.hands[player]}

        hand.remove(card)
        table.difference_update(targets)
        table.add(reduce(or_, {*targets, Unit.from_card(card)}))
        hand.add(deck.pop())

        return replace(self, deck=deck, table=frozenset(table), hands={**self.hands, pl: frozenset(hand)})

    def with_capture(self, player, card, *targets):
        deck = [*self.deck]
        table = {*self.table}
        hand = {*self.hands[player]}

        if not all(card.value == t.value for t in targets):
            raise ValueError(f'cannot capture {targets} with {card}')

        hand.remove(card)
        table.difference_update(targets)
        hand.add(deck.pop())

        return replace(self, deck=deck, table=frozenset(table), hands={**self.hands, pl: frozenset(hand)})

    def render(self):
        return [
            f'Table: {" ".join(u.render() for u in self.table)}',
            *(
                f'{pl.name:<10} {" ".join(c.symbol for c in h)}'
                for pl, h in sorted(self.hands.items(), key=lambda pl_h: pl_h[0].name)
            ),
        ]

if __name__ == '__main__':
    rnd = Random(0)

    deck = [c for c in STANDARD_DECK]
    rnd.shuffle(deck)

    players = {
        Player.from_name(name)
        for name in 'Cameron Emmet Jef Michel'.split()
    }
    state = State.from_players(deck, *players)
    state = state.with_deal()
    print(
        '\n'.join(state.render()),
        sep='\n', end='\n\n',
    )

    pl = [*players][0]

    c = [*state.hands[pl]][0]
    state = state.with_discard(pl, c)

    print(
        f'{pl.name} discards {c.symbol}',
        '\n'.join(state.render()),
        sep='\n', end='\n\n',
    )

    c = [*state.hands[pl]][-1]
    t = [*state.table][-1]
    state = state.with_build(pl, c, t)

    print(
        f'{pl.name} builds {c.symbol} on top of {t.render()}',
        '\n'.join(state.render()),
        sep='\n', end='\n\n',
    )

    c = [*state.hands[pl]][2]
    t = [*state.table][2]
    state = state.with_capture(pl, c, t)

    print(
        f'{pl.name} captures {t.render()} using {c.symbol}',
        '\n'.join(state.render()),
        sep='\n', end='\n\n',
    )
