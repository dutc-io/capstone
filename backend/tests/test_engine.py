from pytest import raises

from engine import game, MissingPlayerException, Player, STANDARD_DECK, Suit, Rank

# Smoke tests (that basically test that pytest is working). But maybe a
# starting porint?

# python hashseed set to 0 via export PYTHONHASHSEED=0

DECK = [c for c in STANDARD_DECK]


def test_suits():

    suits = ["Diamond", "Club", "Heart", "Spade"]

    for s in suits:
        assert Suit[s]

    assert len([*Suit]) == len(suits)


def test_players_from_name():

    player_to_create = "Hyacinth"
    player = Player.from_name(player_to_create)

    assert player.name == player_to_create
    assert player.points == 0


def test_state_from_game():

    player_to_create = "Hyacinth"
    player = Player.from_name(player_to_create)

    state = game([player])

    assert player in state.players
    assert len(state.deck) == 44  # Aftr deal


def test_with_player():

    hyacinth = Player.from_name("Hyacinth")
    state = game([hyacinth])

    with state.players_turn("Hyacinth") as player:
        assert player is hyacinth

    with raises(MissingPlayerException):
        with state.players_turn("Not Hyacinth") as player:
            ...


def test_disguard():
    state = game([Player.from_name("Hyacinth"), Player.from_name("Boonsri")])
    # Inital state for debugging game
    print(
        "\n".join(state.render()),
        sep="\n",
        end="\n",
    )

    with state.players_turn("Hyacinth") as player:
        card = [*state.hands[player]][0]  # K<clubs>
        state = state.with_discard(player, card)
        assert card not in [*state.hands[player]]

    # Discarded state for debugging game
    print(" ")
    print(
        f"{player.name} discards {card.symbol}",
        "\n".join(state.render()),
        sep="\n",
        end="\n\n",
    )


def test_with_build():
    deck = [d for d in DECK if d.rank in [Rank.Two, Rank.Three, Rank.Five]]
    state = game([Player.from_name("Hyacinth")], _deck=deck)
    # Inital state for debugging game
    print(
        "\n".join(state.render()),
        sep="\n",
        end="\n",
    )

    with state.players_turn("Hyacinth") as player:
        card = [*state.hands[player]][0]  # 5<spade>
        target = [*state.table][0]  # 3<club>
        state = state.with_build(player, card, target)
        assert card not in [*state.hands[player]]
        
        assert card in {c for c in [*state.table][0].cards}
        assert [*target.cards][0] in {c for c in [*state.table][0].cards}

    print(" ")
    print(
        f"{player.name} builds on {' '.join([c.symbol for c in target.cards])} with {card.symbol}",
        "\n".join(state.render()),
        sep="\n",
        end="\n\n",
    )

def test_with_capture():
    deck = [d for d in DECK if d.rank in [Rank.Two, Rank.Three, Rank.Five]]
    state = game([Player.from_name("Hyacinth")], _deck=deck)
    # Inital state for debugging game
    print(
        "\n".join(state.render()),
        sep="\n",
        end="\n",
    )

    with state.players_turn("Hyacinth") as player:
        card = [*state.hands[player]][0]  # 5<spade>
        target = [*state.table][1]  # 5<diamond>
        state = state.with_capture(player, card, target)
        assert card not in [*state.hands[player]]
        assert [*target.cards][0] not in {c for u in [*state.table] for c in u.cards}
        assert len([*state.table]) == 3

    print(" ")
    print(
        f"{player.name} captures {' '.join([c.symbol for c in target.cards])} with {card.symbol}",
        "\n".join(state.render()),
        sep="\n",
        end="\n\n",
    )
