from player import Player, RandomBot, MinimaxBot
from constants import Color


def test_init_player():
    player = Player(Color.WHITE)
    assert player.color == Color.WHITE
    assert not player.ai


def test_init_randombot():
    player = RandomBot(Color.WHITE)
    assert player.color == Color.WHITE
    assert player.ai


def test_map_fields_to_pixels():
    player = RandomBot(Color.WHITE)
    assert player.map_field_cords_to_pixels((5, 3)) == (412.5, 262.5)


def test_minimaxbot_init_and_methods():
    player = MinimaxBot(Color.WHITE)
    assert player.ai
    assert player.color == Color.WHITE
    assert player.minimizing_or_maximizing(Color.WHITE)
    assert not player.minimizing_or_maximizing(Color.BLACK)
