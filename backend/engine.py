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


class Suit(Enum):
    Diamond = "Diamond"
    Club = "Club"
    Heart = "Heart"
    Spade = "Spade"


class Rank(Enum):
    Two = "Two"
    Three = "Three"
    Four = "Four"
    Five = "Five"
    Six = "Six"
    Seven = "Seven"
    Eight = "Eight"
    Nine = "Nine"
    Ten = "Ten"
    Jack = "Jack"
    Queen = "Queen"
    King = "King"
    Ace = "Ace"


class Card(BaseModel):
    rank: Rank
    suit: Suit

    SUITS: ClassVar[dict] = {
        "Diamond": "\N{black diamond suit}",
        "Club": "\N{black club suit}",
        "Heart": "\N{black heart suit}",
        "Spade": "\N{black spade suit}",
    }
    RANKS: ClassVar[dict] = {
        "Two": " 2 ",
        "Three": " 3 ",
        "Four": " 4 ",
        "Five": " 5 ",
        "Six": " 6 ",
        "Seven": " 7 ",
        "Eight": " 8 ",
        "Nine": " 9 ",
        "Ten": " 10",
        "Jack": " J ",
        "Queen": " Q ",
        "King": " K ",
        "Ace": " A ",
    }
    VALUES: ClassVar[dict] = {
        "Ace": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
        "Six": 6,
        "Seven": 7,
        "Eight": 8,
        "Nine": 9,
        "Ten": 10,
        "Jack": 10,
        "Queen": 10,
        "King": 10,
    }

    class Config:
        # keep_untouched = (cached_property,)
        use_enum_values = True

    @property
    def value(self):
        return self.VALUES[self.rank]

    @property
    def symbol(self):
        if self.suit in {"Heart", "Diamond"}:
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
    cards: List[Card]
    value: int | None = None

    def __hash__(self):
        return hash((tuple(self.cards), self.value))

    @classmethod
    def from_card(cls, card):
        return cls(cards=[card], value=card.value)

    def render(self):
        if len(self.cards):
            return "【{}】".format(" ".join(c.symbol.lstrip() for c in self.cards))
        return " ".join(c.symbol for c in self.cards)

    def __or__(self, other):
        if self.value is None or other.value is None:
            raise ValueError("cannot combine")
        if (self.value + other.value) > max(Card.VALUES.values()):
            raise ValueError("cannot combine")
        return Unit(cards=[*self.cards, *other.cards], value=self.value + other.value)


class State(BaseModel):
    deck: list[Card]
    table: list[Unit]
    # XXX: Validate no more then six
    players: list[Player]
    player_order: List[Player]
    hands: Dict[str, List[Card]] 
    capture: Dict[str, List[Card]] | None = None

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

        player = self.player_order.pop(0)
        try:
            yield player
        finally:
            self.player_order.append(player)

    @classmethod
    def from_players(cls, deck, players):
        # XXX: We should fix how this deals and go 2 at a time to everyone.

        player_order = players

        hands = defaultdict(list)
        for p in players:
            for _ in range(2):
                card_one = deck.pop()
                card_two = deck.pop()
                hands[p.name].append(card_one)
                hands[p.name].append(card_two)

        table = [Unit.from_card(deck.pop()) for _ in range(4)]
        hands = {pl_name: cards for pl_name, cards in hands.items()}

        return cls(
            deck=deck,
            table=table,
            players=players,
            hands=hands,
            capture={pl.name: [] for pl in players},
            player_order=player_order,
        )

    def with_discard(self, player, card_idx):
        with self.players_turn(player) as current_player:
            deck = [*self.deck]
            table = [*self.table]
            hands = {}
            for pl_name, h in self.hands.items():
                # Discard
                # XXX: Ugly string compareison... What if two players have the same name
                if pl_name == current_player.name:
                    # Players hand
                    hand = [*self.hands[current_player.name]]
                    # The card to discard to the table
                    # Remove from players hand
                    card = hand.pop(card_idx)
                    # Add to the tables hand
                    table.append(Unit.from_card(card))
                    # Deal the player another card automatically
                    hand.append(deck.pop())
                    # Replace the players hand with the new hand
                    hands[current_player.name] = hand
                else:
                    # Not the player so just keep everything the same
                    hands[pl_name] = h

        # This introduces the df = df(...) idea. Should we write our own
        # replace? This feels kinda clumbsy.
        return State(
            deck=deck,
            table=table,
            players=self.players,
            hands=hands,
            capture=self.capture,
            player_order=self.player_order,
        )

    def with_build(self, player, card_idx, target_idx):
        with self.players_turn(player) as current_player:
            deck = self.deck
            table = self.table
            hand = self.hands[current_player.name]

            card = hand.pop(card_idx)
            # Add a card to the table unit
            table[target_idx].cards.append(card)
            hand.append(deck.pop())

        return State(
            deck=deck,
            table=table,
            players=self.players,
            hands={**self.hands, current_player.name: hand},
            capture=self.capture,
            player_order=self.player_order,
        )

    def with_capture(self, player, card_idx, target_idx):
        with self.players_turn(player) as current_player:
            deck = self.deck
            table = self.table
            hand = self.hands[current_player.name]
            capture = self.capture[current_player.name]

            card = hand.pop(card_idx)

            if not all(u.value == card.value for u in table[target_idx].cards):
                raise ValueError(f"cannot capture {target_idx} with {card}")

            # Capture was successful, remove the card and the table card
            # XXX: Need to add this to capture
            table_unit_captured = table.pop(target_idx)

            # Not sure what capture should look like
            capture.append(table_unit_captured)

            hand.append(deck.pop())

        return State(
            deck=deck,
            table=table,
            players=self.players,
            hands={**self.hands, current_player.name: hand},
            capture={**self.capture, current_player.name: capture},
            player_order=self.player_order,
        )

    def render(self):
        # XXX: Make these line up! This is so annoying
        return "".join(
            [
                "",
                f"Current Turn: {self.player_order[0].name}\n",
                f"Table: {' '.join(u.render() for u in self.table)}\n",
                *(
                    f"\n{p:<8} {'  '.join(c.symbol for c in h)} \n"
                    for p, h in sorted(self.hands.items(), key=lambda pl_h: pl_h)
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
    state = State.from_players(deck, players)

    return state


if __name__ == "__main__":

    players = [
        Player(name="Hyacinth"),
        Player(name="Rose"),
        Player(name="Daisy"),
        Player(name="Onslow"),
    ]
    state = game(players)

    serilaized = state.dict()

    state = State(**serilaized)
    print(state.render())
    print(" ")
    # print(state.render())
    # state = state.with_discard("Hyacinth", 1)
    # print(" ")
    # # print(state.render())
    # state = state.with_discard("Rose", 1)
    # print(" ")
    # # print(state.render())
    # state = state.with_discard("Daisy", 1)
    # print(" ")
    # # print(state.render())
    # state = state.with_capture("Onslow", 1, 2)
    #
    # print(" ")
    # # print(state.render())
    # state = state.with_build("Hyacinth", 1, 0)
    #
    # print(state.render())
    # from json import dump
    #
    # with open("state_dump.json", "wt") as fp:
    #     dump(state.dict(), fp, indent=2)
