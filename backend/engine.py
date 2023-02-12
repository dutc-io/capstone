#!/usr/bin/env python3
from enum import Enum
from random import Random
from typing import Dict, List, ClassVar, Union
from operator import or_
from functools import cached_property, reduce
from itertools import islice, product, tee
from contextlib import contextmanager
from collections import defaultdict, deque

from pydantic import BaseModel

nwise = lambda g, *, n=2: zip(*(islice(g, i, None) for i, g in enumerate(tee(g, n))))


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


class Card(BaseModel):
    rank: Rank
    suit: Suit

    SUITS: ClassVar[dict] = {
        Suit.Diamond: "\N{black diamond suit}",
        Suit.Club: "\N{black club suit}",
        Suit.Heart: "\N{black heart suit}",
        Suit.Spade: "\N{black spade suit}",
    }
    RANKS: ClassVar[dict] = {
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
    VALUES: ClassVar[dict] = {
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
        Rank.Jack: 10,
        Rank.Queen: 10,
        Rank.King: 10,
    }

    class Config:
        keep_untouched = (cached_property,)

    @cached_property
    def value(self):
        return self.VALUES[self.rank]

    @cached_property
    def symbol(self):
        if self.suit in {Suit.Heart, Suit.Diamond}:
            return (
                f"\033[1;41m{self.RANKS[self.rank]}{self.SUITS[self.suit]} \033[1;37;0m"
            )
        return f"\033[1;7m{self.RANKS[self.rank]}{self.SUITS[self.suit]} \033[1;37;0m"

    def __hash__(self):
        return hash((self.rank, self.suit))


STANDARD_DECK = [Card(rank=r, suit=s) for r, s in product(Rank, Suit)]


class Player(BaseModel):
    name: str
    points: int = 0

    def __hash__(self):
        # XXX: Hmmm... Can their be two players with the same name?
        return hash((self.name, self.points))


class Unit(BaseModel):
    cards: frozenset
    value: int | None = None

    def __hash__(self):
        return hash((self.cards, self.value))

    @classmethod
    def from_card(cls, card):
        return cls(cards=frozenset(card), value=card.value)

    def render(self):
        if len(self.cards):
            # XXX Need nwise rank/suit
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


class State(BaseModel):
    deck: deque[Card]
    table: list[Unit]
    # XXX: Validate no more then six
    players: list[Player]
    player_order: List[Player]
    hands: dict # Dict[Player, frozenset] | None = None
    capture: Dict[Player, frozenset] | None = None

    @contextmanager
    def players_turn(self, player_name):
        _player = None
        for p in self.players:
            if p.name == player_name:
                _player = p
                break

        if not _player:
            raise MissingPlayerException(f"Could not find player {player_name!r}")

        # XXX: Think about the equality here
        if _player != self.player_order[0]:
            raise NotTurnException(f"Not {player_name!r}'s turn")

        player = self.player_order.popleft()
        try:
            yield player
        finally:
            self.player_order.append(player)

    @classmethod
    def from_players(cls, deck, *players):

        _players = frozenset(players)
        player_order = list(players)

        hands = defaultdict(list)
        for p in players:
            for _ in range(2):
                card_one = deck.pop()
                card_two = deck.pop()
                hands[p].append(card_one)
                hands[p].append(card_two)
        
        table = [Unit.from_card(deck.pop()) for _ in range(4)]
        hands = {pl: cards for pl, cards in hands.items()}
        
        return cls(
            deck=deck,
            table=table,
            players=players,
            hands=hands,
            capture={pl: frozenset() for pl in players},
            player_order=player_order
        )

    def with_discard(self, player, card_idx):
        deck = deque([*self.deck])
        table = [*self.table]
        hands = {}
        for pl, h in self.hands.items():
            # Discard
            if pl.name == player.name:
                # Players hand
                hand = [*self.hands[player]]
                # The card to discard to the table
                card = hand[card_idx]
                # Remove from players hand
                hand.remove(card)
                # Add to the tables hand
                print(card)
                table.append(Unit.from_card(card))
                # Deal the player another card automatically
                hand.append(deck.pop())
                # Replace the players hand with the new hand
                hands[pl] = hand
            else:
                # Not the player so just keep everything the same
                hands[pl] = h

        # This introduces the df = df(...) idea. Should we write our own
        # replace? This feels kinda clumbsy.
        return State(
            deck=deck,
            table=frozenset(table),
            players=self.players,
            hands=hands,
            capture=self.capture,
            player_order=self.player_order,
        )

    # def with_build(self, player, card, *targets):
    #     deck = [*self.deck]
    #     table = {*self.table}
    #     hand = {*self.hands[player]}
    #
    #     hand.remove(card)
    #     table.difference_update(targets)
    #     table.add(reduce(or_, {*targets, Unit.from_card(card)}))
    #     hand.add(deck.pop())
    #
    #     return replace(
    #         self,
    #         deck=deck,
    #         table=frozenset(table),
    #         hands={**self.hands, player: frozenset(hand)},
    #     )
    #
    # def with_capture(self, player, card, *targets):
    #     deck = [*self.deck]
    #     table = {*self.table}
    #     hand = {*self.hands[player]}
    #
    #     if not all(card.value == t.value for t in targets):
    #         raise ValueError(f"cannot capture {targets} with {card}")
    #
    #     hand.remove(card)
    #     table.difference_update(targets)
    #     hand.add(deck.pop())
    #
    #     return replace(
    #         self,
    #         deck=deck,
    #         table=frozenset(table),
    #         hands={**self.hands, player: frozenset(hand)},
    #     )

    def render(self):
        # XXX: Make these line up! This is so annoying
        return "".join(
            [
                "",
                f"Current Turn: {self.player_order[0].name}\n",
                f"Table: {' '.join(u.render() for u in self.table)}\n",
                *(
                    f"\n{p.name:<8} {'  '.join(c.symbol for c in h)} \n"
                    for p, h in sorted(
                        self.hands.items(), key=lambda pl_h: pl_h[0].name
                    )
                ),
            ]
        )


def game(players, seed=0, _deck=None):
    rnd = Random(seed)
    if _deck:
        deck = _deck
    else:
        deck = [c for c in STANDARD_DECK]
        rnd.shuffle(deck)
    state = State.from_players(deque(deck), *players)

    return state


if __name__ == "__main__":

    players = [
        Player(name="Hyacinth"),
        Player(name="Rose"),
        Player(name="Daisy"),
        Player(name="Onslow"),
    ]
    state = game(players)

    print(f"{ state.dict()   = }")

    # from json import dump
    # with open("state_dump.json", "wt") as fp:
    #     dump(state.dict(), fp, indent=2)

    print(state.render())

    # print(" ")
    # with state.players_turn("Hyacinth") as player:
    #     state = state.with_discard(player, 1)
    #
    #
    # print(state.render())
