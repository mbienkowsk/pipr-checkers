from field import Field
from piece_move_board import Piece


class Board:
    def __init__(self) -> None:
        #   optional parameter for a specific setting of the pieces?
        self._fields = None
        self._setup_fields()

    def get_field_by_location(self, location) -> 'Field':
        for row in self.fields:
            for field in row:
                if field.location == location:
                    return field
        return None

    def _setup_fields(self):
        self.fields = [[] for i in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.fields[i].append(Field('white', i, j))
                else:
                    self.fields[i].append(Field('black', i, j))

    def setup_pieces(self):
        for i in range(3):
            for j in range(8):
                current_field = self.board.fields[i][j]
                if current_field.color == 'black':
                    piece = Piece('black', i, j)
                    current_field.piece = piece
                    # self.player_by_color('black').pieces.append(piece)

        for i in range(5, 8):
            for j in range(8):
                current_field = self.board.fields[i][j]
                if current_field.color == 'black':
                    piece = Piece('white', i, j)
                    current_field.piece = piece
                    # self.player_by_color('white').pieces.append(piece)

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, new_fields):
        self._fields = new_fields

    def __str__(self) -> str:
        #   to delete later, for testing purposes
        result = ''
        for row in self.fields:
            for field in row:
                result += str(field)
            result += '\n'
        return result
