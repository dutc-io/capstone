# Capstone 

## Goals

1. For two or more people (up to six) to be able to play a card game for fun.
2. For the contributors to the project to be noticed & to have an opportunity to show off what they know.

## Requirements

- simultaneous play
- hosted
- some rule enforcement
- single variant
- simplification: one single game

## Non-Requirements/Assumptions

- computer-play (bot)
- play other card games
- fixed plays throughout (no joining/leaving)
- don't belabour the mechanics of, e.g., shuffling/dealing

## Design

1. Go to the website.
2. Start a new game → /url/4283123/start
    - How many users.
3. Current game display.
    - Representation of the table.
    - Representation of your hand.
    - Representation of the other plays.
    - Play a card.

## Technical Design

- Javascript interaction (→ React)
- Backend API server
    - Websockets

```python

@dataclass
class Where:
    expr : object

@dataclass
class Select:
    table : str
    columns : list[str]
    where : Where

    def __str__(self):
        return f'select {", ".join(self.columns)} from {self.table!s} where {self.where!s}'

    def __repr__(self):
        return f'Select({self.table!r}, {self.columns!r}, {self.where!r})'

q = Select('employees', ['name', 'salary'], 'not manager')
print(f'{q = !r}')
print(f'{q = !s}')

breakpoint()

```
