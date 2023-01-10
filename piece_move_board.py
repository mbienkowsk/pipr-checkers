from dataclasses import dataclass
# from board import Board
from typing import Tuple
from field import Field
from constants import BEIGE, BROWN, FIELD_SIZE


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

    def set_possible_moving_directions_x(self):
        '''sets the parameters which determine whether a piece can move
        to a square with a higher and lower x than its current square
        '''
        if self.x == 7:
            self.can_move_pos_x = False
        else:
            self.can_move_pos_x = True

        if self.x == 0:
            self.can_move_neg_x = False
        else:
            self.can_move_neg_x = True

    def set_possible_moving_directions_y(self):
        '''sets the parameters which determine whether a piece can move
        to a square with a higher and lower x than its current square
        '''
        if self.king:
            if self.x == 7:
                self.can_move_pos_y = False
            if self.x == 0:
                self.can_move_neg_y = False
            else:
                self.can_move_pos_y = True
                self.can_move_neg_y = True
        else:
            if self.move_constant == 1:
                self.can_move_pos_y = True
                self.can_move_neg_y = False
            else:
                self.can_move_pos_y = False
                self.can_move_neg_y = True

    def all_possible_non_attacking_moves(self):
        '''returns the basic forward(or backward if it's a king) moves a piece
        could possibly make, not taking in consideration whether they're legal
        '''
        moves = list()
        self.set_possible_moving_directions_x()
        self.set_possible_moving_directions_y()
        x = self.x
        y = self.y

        if self.can_move_pos_x:
            if self.can_move_pos_y:
                moves.append(Move(False, (x, y), (x + 1, y + 1), self))
            if self.can_move_neg_y:
                moves.append(Move(False, (x, y), (x + 1, y - 1), self))
        if self.can_move_neg_x:
            if self.can_move_pos_y:
                moves.append(Move(False, (x, y), (x - 1, y + 1), self))
            if self.can_move_neg_y:
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
        if self.move_constant == -1:
            return False
        elif self.x == 7 or self.y == 7:
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
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken:
                    return True
                return False

    def can_attack_plus_minus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y-1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if self.move_constant == 1:
            return False
        elif self.x == 7 or self.y == 0:
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
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken:
                    return True
                return False

    def can_attack_minus_plus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y-1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if self.move_constant == -1:
            return False
        elif self.x == 0 or self.y == 7:
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
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken:
                    return True
                return False

    def can_attack_minus_minus(self, board: 'Board'):
        '''checks whether it's possible to attack a field with coordinates (x+1, y-1)
        if an enemy piece is on the field and the field behind it is empty, returns True
        '''
        if self.move_constant == 1:
            return False
        elif self.x == 0 or self.y == 0:
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
                if field_to_attack.piece.color != self.color and not field_to_jump_to.is_taken:
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
        if move.attacking:
            pass
        else:
            piece.x, piece.y = move.new_cords
            self.get_field_by_location(move.old_cords).piece = None
            self.get_field_by_location(move.new_cords).piece = piece
