from piece_move_board import Board, Move  # , Piece
from constants import Color, BROWN, BEIGE
from copy import copy


def test_board_init():
    board = Board()
    assert len(board.fields) == 8
    assert len(board.fields[0]) == 8
    assert board.moves_without_attacks == 0

    expected_occupied_fields_coords = {
        (0, 1),
        (0, 5),
        (0, 7),
        (1, 0),
        (1, 2),
        (1, 6),
        (2, 1),
        (2, 5),
        (2, 7),
        (3, 0),
        (3, 2),
        (3, 6),
        (4, 1),
        (4, 5),
        (4, 7),
        (5, 0),
        (5, 2),
        (5, 6),
        (6, 1),
        (6, 5),
        (6, 7),
        (7, 0),
        (7, 2),
        (7, 6)
    }

    actual_occupied_field_coords = set()
    for row in board.fields:
        for field in row:
            if field.is_taken():
                actual_occupied_field_coords.add(field.location)
    assert len(expected_occupied_fields_coords) == len(actual_occupied_field_coords)
    assert expected_occupied_fields_coords == actual_occupied_field_coords
    assert not board.is_game_over
    assert board.turn == Color.WHITE
    assert not (board.mandatory_attacks[Color.WHITE] and board.mandatory_attacks[Color.BLACK])


def test_get_field_by_location():
    board = Board()
    field_at_3_2 = board.get_field_by_location((3, 2))
    assert field_at_3_2.x == 3
    assert field_at_3_2.y == 2


def test_delete_piece():
    board = Board()
    field_to_delete_from = board.get_field_by_location((0, 1))
    piece_to_delete = field_to_delete_from.piece
    assert piece_to_delete.color == Color.BLACK
    board.delete_piece(piece_to_delete)
    assert not board.get_field_by_location((0, 1)).is_taken()
    assert len(board.all_black_pieces()) == 11
    assert piece_to_delete not in board.pieces_by_colors[Color.BLACK]
    assert piece_to_delete not in board.moves_by_colors[Color.BLACK]


def test_one_dimensional_field_list():
    board = Board()
    assert len(board.one_dimensional_field_list) == 64
    brown_fields = [field for field in board.one_dimensional_field_list
                    if field.color == BROWN]
    beige_fields = [field for field in board.one_dimensional_field_list
                    if field.color == BEIGE]
    assert len(brown_fields) == len(beige_fields) == 32


def test_all_pieces_of_color_x():
    board = Board()
    assert len(board.all_white_pieces()) == len(board.all_black_pieces()) == 12
    field_to_delete_from = board.get_field_by_location((0, 1))
    piece_to_delete_white = field_to_delete_from.piece
    board.delete_piece(piece_to_delete_white)
    field_to_delete_from = board.get_field_by_location((0, 7))
    piece_to_delete_black = field_to_delete_from.piece
    board.delete_piece(piece_to_delete_black)
    assert len(board.all_white_pieces()) == len(board.all_black_pieces()) == 11
    assert piece_to_delete_black not in board.all_black_pieces()
    assert piece_to_delete_white not in board.all_white_pieces()


def test_update_possible_moves_by_colors():
    board = Board()
    piece_to_move = board.get_field_by_location((0, 5)).piece
    board.handle_move(Move(False, piece_to_move.location, (1, 4), piece_to_move))
    assert len(board.moves_by_colors[piece_to_move.color][piece_to_move]) == 2
    assert Move(False, (1, 4), (0, 3), piece_to_move) in board.moves_by_colors[piece_to_move.color][piece_to_move]
    assert Move(False, (1, 4), (2, 3), piece_to_move) in board.moves_by_colors[piece_to_move.color][piece_to_move]


def test_handle_move():
    board = Board()
    piece_to_move = board.get_field_by_location((0, 5)).piece
    possible_moves = board.moves_by_colors[piece_to_move.color][piece_to_move]
    assert len(possible_moves) == 1
    board.handle_move(Move(False, piece_to_move.location, (1, 4), piece_to_move))
    assert piece_to_move.location == (1, 4)
    assert board.turn == Color.BLACK


def test_all_possible_children_boards():
    board = Board()
    number_of_moves_for_white = 0
    for piece in board.all_white_pieces():
        number_of_moves_for_white += len(board.moves_by_colors[Color.WHITE][piece])
    assert len(board.all_possible_children_boards(Color.WHITE)) == number_of_moves_for_white


def test_evaluate_position():
    board = Board()
    assert board.evaluate_position() == 0
    piece_to_del = board.get_field_by_location((0, 7)).piece
    board.delete_piece(piece_to_del)
    assert board.evaluate_position() == -3
    piece_to_promote = board.get_field_by_location((7, 6)).piece
    piece_to_promote.promote()
    assert board.evaluate_position() == -1


def test_player_has_moving_options_and_winner():
    board = Board()
    assert board.player_has_moving_options(Color.WHITE)
    assert len(board.all_white_pieces()) == 12
    white_pieces = copy(board.all_white_pieces())
    for piece in white_pieces:
        board.delete_piece(piece)
    assert len(board.all_white_pieces()) == 0
    assert not board.player_has_moving_options(Color.WHITE)
    assert board.winner() == Color.BLACK


def test_change_turn():
    board = Board()
    board.change_turn()
    assert board.turn == Color.BLACK


def test_jumped_piece_and_has_to_jump():
    board = Board()
    first_piece = board.get_field_by_location((0, 5)).piece
    first_move = Move(False, (0, 5), (1, 4), first_piece)
    board.handle_move(first_move)
    assert board.moves_without_attacks == 1

    second_piece = board.get_field_by_location((3, 2)).piece
    second_move = Move(False, (3, 2), (2, 3), second_piece)
    board.handle_move(second_move)

    assert len(board.moves_by_colors[Color.WHITE][first_piece]) == 1
    attacking_move = board.moves_by_colors[Color.WHITE][first_piece][0]
    assert board.get_jumped_piece(attacking_move) == second_piece
