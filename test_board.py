from board import Board


def test_board_init():
    board = Board()
    assert len(board.fields) == 8
    assert len(board.fields[0]) == 8
    # for row in range(3):
    #     for col in range(8):
    #         if (row + col) % 2 == 0:
