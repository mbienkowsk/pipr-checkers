from checkers.game import Game
from checkers.player import Player, MinimaxBot
from checkers.constants import Color, Placeholder, SLEEP_TIME_IN_PVB_GAME


def test_game_init(monkeypatch):
    monkeypatch.setattr('checkers.game.Game.load_images', lambda x: None)
    player1 = Player(Color.WHITE)
    player2 = Player(Color.BLACK)
    game = Game(Placeholder.SCREEN, [player1, player2])

    assert game.player_color_dictionary == {
        Color.WHITE: player1,
        Color.BLACK: player2
    }

    assert not game.sleep_duration
    assert not game.selected_piece
    assert game.screen == Placeholder.SCREEN


def test_game_interpret_clicked_location(monkeypatch):
    monkeypatch.setattr('checkers.game.Game.load_images', lambda x: None)
    player1 = Player(Color.WHITE)
    player2 = MinimaxBot(Color.BLACK, None, None)
    game = Game(Placeholder.SCREEN, [player1, player2])
    assert game.sleep_duration == SLEEP_TIME_IN_PVB_GAME

    click_location_1 = (70, 70)
    clicked_field = game.board.get_field_by_location((0, 0))
    clicked_piece = clicked_field.piece
    assert (game.interpret_clicked_pixel_location(click_location_1)
            == (clicked_field, clicked_piece))
