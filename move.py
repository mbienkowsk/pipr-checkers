from piece import Piece


class Move:
    def __init__(
        self, attacking: bool,
        old_cords: tuple(int), new_cords: tuple(int),
        piece: 'Piece'):

        self.attacking = attacking
        self.old_cords = old_cords
        self.new_cords = new_cords
        self.piece = piece
