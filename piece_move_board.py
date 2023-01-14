from dataclasses import dataclass
from typing import Tuple
from field import Field
from constants import BEIGE, BROWN, FIELD_SIZE, NUM_OF_COLUMNS, NUM_OF_ROWS
from errors import NonexistingFieldCallError


class Piece:
    def __init__(self, color, x, y) -> None:
        self._value = 1
        self._king = False
        self.color = color
        self._x = x
        self._y = y

        if self.color == 'white':
            self.image_dict_ind = 'WP'
        else:
            self.image_dict_ind = 'BP'

    def promote(self):
        '''promote a piece to a king piece and set the right attributes
        to some of its values
        '''
        self.king = True
        self.value = 2  # not sure if 2 is the right evaluation
        if self.image_dict_ind == 'WP':
            self.image_dict_ind = 'WK'
        else:
            self.image_dict_ind = 'BK'

    def eligible_for_promotion_after_move(self, move):
        '''Checks whether making the given move, the piece
        will land on the last rank, resulting in it being promoted to a king
        '''
        new_y = move.new_cords[1]
        if new_y in (0, NUM_OF_ROWS - 1) and not self.king:
            return True
        return False

    @property
    def move_constant(self):
        '''The value of y added to the location of a piece
        during a move - white is on the bottom of the board by
        default, so the y should be decremented, reversed for black
        if a piece is a king, the const is 0, representing it has no
        set direction to move to
        '''
        if self.king:
            return 0
        else:
            return -1 if self.color == 'white' else 1

    def can_move_plus_x(self, attack=False):
        if attack:
            cols_where_cannot = [NUM_OF_COLUMNS - 2, NUM_OF_COLUMNS - 1]
        else:
            cols_where_cannot = [NUM_OF_COLUMNS - 1]
        return self.x not in cols_where_cannot

    def can_move_minus_x(self, attack=False):
        if attack:
            cols_where_cannot = [0, 1]
        else:
            cols_where_cannot = [0]
        return self.x not in cols_where_cannot

    def can_move_plus_y(self, attack=False):
        if self.move_constant == -1:
            return False
        if attack:
            rows_where_cannot = [NUM_OF_ROWS - 2, NUM_OF_ROWS - 1]
        else:
            rows_where_cannot = [NUM_OF_ROWS - 1]
        return self.y not in rows_where_cannot

    def can_move_minus_y(self, attack=False):
        # FIXME
        if self.move_constant == 1:
            return False
        if attack:
            rows_where_cannot = [0, 1]
        else:
            rows_where_cannot = [0]
        return self.y not in rows_where_cannot

    def all_possible_non_attacking_moves(self):
        '''returns the basic forward(or backward if it's a king) moves a piece
        could possibly make, not taking in consideration whether they're legal
        '''
        moves = list()
        x = self.x
        y = self.y

        if self.can_move_plus_x():
            if self.can_move_plus_y():
                moves.append(Move(False, (x, y), (x + 1, y + 1), self))
            if self.can_move_minus_y():
                moves.append(Move(False, (x, y), (x + 1, y - 1), self))
        if self.can_move_minus_x():
            if self.can_move_plus_y():
                moves.append(Move(False, (x, y), (x - 1, y + 1), self))
            if self.can_move_minus_y():
                moves.append(Move(False, (x, y), (x - 1, y - 1), self))
        return moves

    def all_legal_non_attacking_moves(self, board: 'Board'):
        '''returns the list of legal non attacking moves
        '''
        legal_moves = []
        for move in self.all_possible_non_attacking_moves():
            location_to_move = move.new_cords
            field_to_move = board.get_field_by_location(location_to_move)
            if not field_to_move.is_taken():
                legal_moves.append(move)
        return legal_moves

    def can_attack_plus_plus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y+1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if not (self.can_move_plus_x(attack=True) and self.can_move_plus_y(attack=True)):
            return False
        else:
            field_to_attack = board.get_field_by_location(
                (self.x + 1, self.y + 1)
            )
            field_to_jump_to = board.get_field_by_location(
                (self.x + 2, self.y + 2)
            )
            if not field_to_attack.is_taken():
                return False
            else:
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken():
                    return True
                return False

    def can_attack_plus_minus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y-1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if not (self.can_move_plus_x(attack=True) and self.can_move_minus_y(attack=True)):
            return False
        else:
            field_to_attack = board.get_field_by_location(
                (self.x + 1, self.y - 1)
            )
            field_to_jump_to = board.get_field_by_location(
                (self.x + 2, self.y - 2)
            )
            if not field_to_attack.is_taken():
                return False
            else:
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken():
                    return True
                return False

    def can_attack_minus_plus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y-1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if not (self.can_move_minus_x(attack=True) and self.can_move_plus_y(attack=True)):
            return False
        else:
            field_to_attack = board.get_field_by_location(
                (self.x - 1, self.y + 1)
            )
            field_to_jump_to = board.get_field_by_location(
                (self.x - 2, self.y + 2)
            )
            if not field_to_attack.is_taken():
                return False
            else:
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken():
                    return True
                return False

    def can_attack_minus_minus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y-1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if not (self.can_move_minus_x(attack=True) and self.can_move_minus_y(attack=True)):
            return False
        else:
            field_to_attack = board.get_field_by_location(
                (self.x - 1, self.y - 1)
            )
            field_to_jump_to = board.get_field_by_location(
                (self.x - 2, self.y - 2)
            )
            if not field_to_attack.is_taken():
                return False
            else:
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken():
                    return True
                return False

    def all_legal_attacking_moves(self, board: 'Board'):
        legal_moves = []
        if self.can_attack_plus_plus(board):
            legal_moves.append(Move(True, self.location, (self.x + 2, self.y + 2), self))
        if self.can_attack_minus_plus(board):
            legal_moves.append(Move(True, self.location, (self.x - 2, self.y + 2), self))
        if self.can_attack_plus_minus(board):
            legal_moves.append(Move(True, self.location, (self.x + 2, self.y - 2), self))
        if self.can_attack_minus_minus(board):
            legal_moves.append(Move(True, self.location, (self.x - 2, self.y - 2), self))
        return legal_moves

    def all_possible_legal_moves(self, board: 'Board'):
        '''returns the list of potential legal moves a piece can make,
        taking into consideration the fact that if there are any possible attacks,
        they have to be executed
        '''
        if self.all_legal_attacking_moves(board):
            return self.all_legal_attacking_moves(board)
        else:
            return self.all_legal_non_attacking_moves(board)

    def location_to_draw(self):
        x, y = self.x, self.y
        x_to_draw = x * FIELD_SIZE + 0.5 * FIELD_SIZE
        y_to_draw = y * FIELD_SIZE + 0.5 * FIELD_SIZE
        return (x_to_draw, y_to_draw)

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def king(self):
        return self._king

    @king.setter
    def king(self, val: bool):
        self._king = val

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def location(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        # for testing purposes, to delete later
        return f'{self.location}: {self.color}'


@dataclass(frozen=True)
class Move:
    attacking: bool
    old_cords: Tuple[int, int]
    new_cords: Tuple[int, int]
    piece: Piece


class Board:
    def __init__(self) -> None:
        self._fields = None
        self._setup_fields()
        self._setup_pieces()
        self.pieces_by_colors = dict()
        self.update_pieces_by_colors()
        self.moves_by_colors = dict()
        self.update_possible_moves_by_colors()

    def get_field_by_location(self, location) -> 'Field':
        for row in self.fields:
            for field in row:
                if field.location == location:
                    return field
        raise NonexistingFieldCallError(f'Tried to obtain a nonexisting field: {location}')

    def _setup_fields(self):
        self.fields = [[] for i in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.fields[i].append(Field(BEIGE, i, j))
                else:
                    self.fields[i].append(Field(BROWN, i, j))

    def _setup_pieces(self):
        for i in range(3):
            for j in range(8):
                current_field = self.fields[j][i]
                if current_field.color == BROWN:
                    piece = Piece('black', j, i)
                    current_field.piece = piece
                    # self.player_by_color('black').pieces.append(piece)

        for i in range(5, 8):
            for j in range(8):
                current_field = self.fields[j][i]
                if current_field.color == BROWN:
                    piece = Piece('white', j, i)
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

    def move_piece(self, piece, move):
        if move.attacking:  # do we need the separation?
            piece.x, piece.y = move.new_cords
            self.get_field_by_location(move.old_cords).piece = None
            self.get_field_by_location(move.new_cords).piece = piece
        else:
            piece.x, piece.y = move.new_cords
            self.get_field_by_location(move.old_cords).piece = None
            self.get_field_by_location(move.new_cords).piece = piece

    def delete_piece(self, piece):
        piece_field = self.get_field_by_location(piece.location)
        piece_field.piece = None

    @property
    def one_dimensional_field_list(self):
        field_list = list()
        for row in self.fields:
            for field in row:
                field_list.append(field)
        return field_list

    def update_pieces_by_colors(self):
        pieces_by_colors = {
            'white': [],
            'black': []
        }
        for field in self.one_dimensional_field_list:
            if field.is_taken():
                current_piece = field.piece
                pieces_by_colors[current_piece.color].append(current_piece)
        self.pieces_by_colors = pieces_by_colors

    def all_white_pieces(self):
        return self.pieces_by_colors['white']

    def all_black_pieces(self):
        return self.pieces_by_colors['black']

    def player_has_to_attack(self, color):
        player_dict = self.moves_by_colors[color]
        for value in player_dict.values():
            for move in value:
                if move.attacking:
                    return True
        return False

    def update_possible_moves_by_colors(self):

        moves_by_colors = {
            'white': {},
            'black': {}
        }

        for piece in self.all_white_pieces():
            moves_by_colors['white'][piece] = piece.all_possible_legal_moves(self)
        for piece in self.all_black_pieces():
            moves_by_colors['black'][piece] = piece.all_possible_legal_moves(self)

        self.moves_by_colors = moves_by_colors

        if self.player_has_to_attack('white'):
            for piece in self.all_white_pieces():
                moves_by_colors['white'][piece] = [move for move in piece.all_possible_legal_moves(self) if move.attacking]

        if self.player_has_to_attack('black'):
            for piece in self.all_black_pieces():
                moves_by_colors['black'][piece] = [move for move in piece.all_possible_legal_moves(self) if move.attacking]

        self.moves_by_colors = moves_by_colors

    def feasible_locations_and_moves_for_piece(self, piece):
        self.update_possible_moves_by_colors()
        moves = self.moves_by_colors[piece.color][piece]
        locations = [move.new_cords for move in moves]
        return locations, moves

    def can_piece_move(self, piece):
        '''Determines whether a piece can be moved during a player's turn
        If the piece can't attack and another one of its color can,
        returns False. Else, returns True
        '''
        if self.player_has_to_attack(piece.color):
            if not piece.all_legal_attacking_moves(self):
                return False
        return True
