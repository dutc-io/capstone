#!/usr/bin/env python3

from functools import total_ordering
from itertools import product
from random import Random

@total_ordering
class OrderedEnum(Enum):
    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self, other):
        return self.value < other.value
    def __hash__(self):
        return hash(self.value)

Value = Enum(
    'Value',
    'Two Three Four Five Six Seven Eight Nine Ten Jack Queen King Ace',
    type=OrderedEnum,
)
Suit = Enum(
    'Suit',
    'Diamond Club Heart Spade',
    type=OrderedEnum,
)
Card = namedtuple('Card', 'value suit')
STANDARD_DECK = [Card(value=v, suit=s) for v, s in product(Value, Suit)]

@dataclass(frozen=True)
class Player:
    name : str
    hand : list = field(default_factory=list)
    capture : set = field(default_factory=set)

    def match_cards(self, suit=None, value=None):
        match suit, value:
            case None, None:
                return self.capture
            case Suit, None:
                return [ c for c in self.capture if c.suit is Suit ]
            case None, Value:
                return [ c for c in self.capture if c.value is Value ]
            case Suit, Value:
                card = Card(suit=Suit, value=Value)
                return [ c for c in self.capture if c == card ]

    def count_cards(self, suit=None, value=None):
        return len(self.match_cards(suit=suit, value=value))

    def show_cards(self, suit=None, value=None):
        return self.match_cards(suit=suit, value=value)

    def __hash__(self):
        return hash(id(self))

# TODO: implement the bonus point
@dataclass(frozen=True, unsafe_hash=True)
class Rule:
    player : Player
    ALL_RULES = {*()}
    def __init_subclass__(cls, points):
        cls.points = points
        cls.ALL_RULES.add(cls)
        if not hasattr(cls, 'from_players'):
            raise TypeError('cls must implement from_players')
    @classmethod
    def from_players(cls, players):
        for r in cls.ALL_RULES:
            yield from r.from_players(players)


@dataclass(frozen=True, unsafe_hash=True)
class MostCards(Rule, points=3):
    @classmethod
    def from_players(cls, players):
        first, second = sorted(players, key=lambda p: p.count_cards(), reverse=True)[:2]
        if first.count_cards() > second.count_cards():
            yield cls(player=first)



@dataclass(frozen=True, unsafe_hash=True)
class MostSpades(Rule, points=1):
    @classmethod
    def from_players(cls, players):
        suit = Suit.Spade
        first, second = sorted(
            players,
            key=lambda p: p.count_cards(suit=suit),
            reverse=True
        )[:2]
        # TODO: eliminate repetition in the below
        if first.count_cards(suit=suit) > second.count_cards(suit=suit):
            yield cls(player=first)

# TODO: eliminate repetition in `BigCassino` and `LittleCassino`
# TODO: try to eliminate repetition in the below with `Ace`

@dataclass(frozen=True, unsafe_hash=True)
class BigCassino(Rule, points=2):
    card : Card

    @classmethod
    def from_players(cls, players):
        target = Card(value=Value.Ten, suit=Suit.Diamond)

        for pl in players:
            if pl.count_cards(value=target.value, suit=target.suit):
                # print("*10D* bigcass", pl.name, target)
                yield cls(player=pl, card=target)



@dataclass(frozen=True, unsafe_hash=True)
class LittleCassino(Rule, points=1):
    card : Card

    @classmethod
    def from_players(cls, players):
        target = Card(value=Value.Two, suit=Suit.Spade)

        for pl in players:
            if pl.count_cards(*target):
                # print("*2S* lilcass", pl.name, target)
                yield cls(player=pl, card=target)


@dataclass(frozen=True, unsafe_hash=True)
class Ace(Rule, points=1):
    card: Card

    @classmethod
    def from_players(cls, players):
        value = Value.Ace

        for pl in players:
            for c in pl.show_cards(value=value):
                # print("*A* aces", pl.name, type(c), c)
                yield cls(player=pl, card=c)

#

if __name__ == '__main__':
    rnd = Random(0)
    deck = [*STANDARD_DECK]
    rnd.shuffle(deck)

    players = {
        Player('Alice'),
        Player('Bob'),
    }


    for c in deck:
        rnd.choice([*players]).capture.add(c)


    rules_by_player = defaultdict(set)

    for r in Rule.from_players(players):
        rules_by_player[r.player].add(r)


    for p, rs in sorted(rules_by_player.items(), key=lambda pl_rs: pl_rs[0].name):
        score = sum(r.points for r in rs)
        if score >= 11:
            score += 1
        print(f'{f"{p.name}:":<10} {score:<3}')

if __name__ == '__main__':
    pass
