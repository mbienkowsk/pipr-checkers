from piece_move_board import Board


def test_board_init():
    board = Board()
    assert len(board.fields) == 8
    assert len(board.fields[0]) == 8

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