from piece_move_board import Piece, Move
from constants import Color


def test_init():
    piece = Piece(Color.WHITE, 7, 6)
    assert piece.value == 3
    assert not piece.king
    assert piece.x == 7
    assert piece.y == 6
    assert piece.location == (7, 6)
    assert piece.image_dict_ind == 'WP'


def test_promote():
    piece = Piece(Color.BLACK, 0, 1)
    piece.promote()
    assert piece.value == 5
    assert piece.image_dict_ind == 'BK'
    assert piece.king


def test_eligible_for_promotion():
    piece = Piece(Color.BLACK, 0, 6)
    move = Move(False, (0, 6), (1, 7), piece)
    assert piece.eligible_for_promotion_after_move(move)


def test_move_constant():
    white_piece_1 = Piece(Color.WHITE, 3, 4)
    white_piece_2 = Piece(Color.WHITE, 6, 7)
    black_piece_1 = Piece(Color.BLACK, 1, 1)
    white_piece_2.promote()
    assert white_piece_1.move_constant == -1
    assert white_piece_2.move_constant == 0
    assert black_piece_1.move_constant == 1


def test_can_move_x():
    white_piece_1 = Piece(Color.WHITE, 3, 4)
    assert white_piece_1.can_move_plus_x()
    assert white_piece_1.can_move_plus_x(attack=True)
    assert white_piece_1.can_move_minus_x()
    assert white_piece_1.can_move_minus_x(attack=True)

    white_piece_2 = Piece(Color.WHITE, 1, 0)
    assert white_piece_2.can_move_plus_x()
    assert white_piece_2.can_move_plus_x(attack=True)
    assert white_piece_2.can_move_minus_x()
    assert not white_piece_2.can_move_minus_x(attack=True)

    white_piece_2 = Piece(Color.WHITE, 6, 0)
    assert white_piece_2.can_move_plus_x()
    assert not white_piece_2.can_move_plus_x(attack=True)
    assert white_piece_2.can_move_minus_x()
    assert white_piece_2.can_move_minus_x(attack=True)


def test_can_move_y():
    white_piece_1 = Piece(Color.WHITE, 3, 4)
    assert white_piece_1.can_move_minus_y()
    assert white_piece_1.can_move_minus_y(True)
    assert not white_piece_1.can_move_plus_y()

    white_piece_1.promote()
    assert white_piece_1.can_move_plus_y(True)

    black_piece_2 = Piece(Color.BLACK, 5, 6)
    assert black_piece_2.can_move_plus_y()
    assert not black_piece_2.can_move_plus_y(True)


def test_all_possible_na_moves():
    black_piece_2 = Piece(Color.BLACK, 5, 5)
    possible_moving_cords = [(6, 6), (4, 6)]

    moves = black_piece_2.all_possible_non_attacking_moves()
    for move in moves:
        assert move.old_cords == black_piece_2.location
        assert move.new_cords in possible_moving_cords


def test_location_to_draw():
    piece = Piece(Color.WHITE, 5, 6)
    assert piece.location_to_draw() == (412.5, 487.5)


