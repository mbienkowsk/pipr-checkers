from dataclasses import dataclass
from typing import Tuple
from field import Field
from constants import BEIGE, BROWN, FIELD_SIZE, NUM_OF_COLUMNS, NUM_OF_ROWS, Color
from errors import NonexistingFieldCallError
from copy import deepcopy


class Piece:
    '''Class representing a checkers piece

    param value: how much is the piece worth during the evaluation of a position
    type value: int

    param king: whether the piece is a king piece
    type king: bool

    param color: the color of the piece
    type color: str FIXME

    param x: the piece's column number
    type x: int

    param y: the piece's row number
    type y: int

    param image_dict_ind: the index mapping the piece onto an image to display in game
    type image_dict_int: str
    '''

    def __init__(self, color, x, y) -> None:
        self._value = 3
        self._king = False
        self.color = color
        self._x = x
        self._y = y

        if self.color == Color.WHITE:
            self.image_dict_ind = 'WP'
        else:
            self.image_dict_ind = 'BP'

    def promote(self):
        '''Promote a piece to a king piece
        sets the value to a higher number and changes its image dict index
        to the one representing the king
        '''
        self.king = True
        self.value = 5
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
            return -1 if self.color == Color.WHITE else 1

    def can_move_plus_x(self, attack=False):
        '''Returns a boolean determining whether the piece has the space to move/attack
        onto a field with a higher x coordinate'''
        if attack:
            cols_where_cannot = [NUM_OF_COLUMNS - 2, NUM_OF_COLUMNS - 1]
        else:
            cols_where_cannot = [NUM_OF_COLUMNS - 1]
        return self.x not in cols_where_cannot

    def can_move_minus_x(self, attack=False):
        '''Returns a boolean determining whether the piece has the space to move/attack
        onto a field with a lower x coordinate'''
        if attack:
            cols_where_cannot = [0, 1]
        else:
            cols_where_cannot = [0]
        return self.x not in cols_where_cannot

    def can_move_plus_y(self, attack=False):
        '''Returns a boolean determining whether the piece can move/attack
        onto a field with a higher y coordinate'''
        if self.move_constant == -1:
            return False
        if attack:
            rows_where_cannot = [NUM_OF_ROWS - 2, NUM_OF_ROWS - 1]
        else:
            rows_where_cannot = [NUM_OF_ROWS - 1]
        return self.y not in rows_where_cannot

    def can_move_minus_y(self, attack=False):
        '''Returns a boolean determining whether the piece can move/attack
        onto a field with a lower y coordinate'''
        # FIXME
        if self.move_constant == 1:
            return False
        if attack:
            rows_where_cannot = [0, 1]
        else:
            rows_where_cannot = [0]
        return self.y not in rows_where_cannot

    def all_possible_non_attacking_moves(self):
        '''Returns the basic forward (and backward if it's a king) moves a piece
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
        '''Takes in the list of non attacking moves and Checks
        whether they're legal
        returns a list of legal moves
        '''
        legal_moves = []
        for move in self.all_possible_non_attacking_moves():
            location_to_move = move.new_cords
            field_to_move = board.get_field_by_location(location_to_move)
            if not field_to_move.is_taken():
                legal_moves.append(move)
        return legal_moves

    def can_attack_plus_plus(self, board: 'Board'):
        '''Checks whether it's possible to attack a field with coordinates (x+1, y+1)
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
        '''Checks whether it's possible to attack a field with coordinates (x+1, y-1)
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
        '''Checks whether it's possible to attack a field with coordinates (x-1, y+1)
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
        '''Checks whether it's possible to attack a field with coordinates (x-1, y-1)
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
        '''
        Returns a list of legal attacking moves a piece can make on a given board
        '''
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
        '''Returns the list of potential legal moves a piece can make,
        taking into consideration the fact that if there are any possible attacks,
        they have to be executed first
        '''
        if self.all_legal_attacking_moves(board):
            return self.all_legal_attacking_moves(board)
        else:
            return self.all_legal_non_attacking_moves(board)

    def location_to_draw(self):
        '''
        Maps the row and column of the piece to a center of its corresponding square
        in the gui checkerboard - the place where the piece is supposed to be displayed
        '''
        x, y = self.x, self.y
        x_to_draw = x * FIELD_SIZE + 0.5 * FIELD_SIZE
        y_to_draw = y * FIELD_SIZE + 0.5 * FIELD_SIZE
        return (x_to_draw, y_to_draw)

    @property
    def value(self):
        '''Getter for the value attribute'''
        return self._value

    @value.setter
    def value(self, value):
        '''Setter for the value attribute'''
        self._value = value

    @property
    def king(self):
        '''Getter for the king attribute'''
        return self._king

    @king.setter
    def king(self, val: bool):
        '''Setter for the king attribute'''
        self._king = val

    @property
    def x(self):
        '''Getter for the x attribute'''
        return self._x

    @x.setter
    def x(self, x):
        '''Setter for the x attribute'''
        self._x = x

    @property
    def y(self):
        '''Getter for the y attribute'''
        return self._y

    @y.setter
    def y(self, y):
        '''Setter for the y attribute'''
        self._y = y

    @property
    def location(self):
        '''Returns the location of a piece - a tuple of its x and y coordinates'''
        return (self.x, self.y)

    def __str__(self) -> str:
        # for testing purposes, to delete later FIXME
        return f'{self.location}: {self.color}'


@dataclass(frozen=True)
class Move:
    '''
    Class representing a checkers move

    param attacking: whether the move involves jumping over an enemy piece
    type attacking: bool

    param old_cords: the location of the piece before the move
    param new_cords: the location of the piece after the move
    type old_cords, new_cords: tuple

    param piece: the piece to be moved
    type piece: Piece'''
    attacking: bool
    old_cords: Tuple[int, int]
    new_cords: Tuple[int, int]
    piece: Piece


class Board:
    '''Class representing a checkers board

    param fields: List of eight lists (rows of the board), each
    with eight fields

    type fields: List[List[Field * 8] * 8]

    param pieces_by_colors: a dictionary mapping a color of a player
    to the list of his piece

    type pieces_by_colors: dict

    param moves_by_colors: a dictionary mapping a color of a player
    to a dictionary with his pieces as keys and their possible moves
    as values

    param turn: the color of the player who is supposed to move at
    the moment

    type turn: string FIXME

    param is_game_over: whether the game is over (can the player
    whoss turn it is make a move?)

    type is_game_over: bool
    '''

    def __init__(self) -> None:
        self._fields = None
        self._setup_fields()
        self._setup_pieces()
        self.pieces_by_colors = dict()
        self.setup_pieces_by_colors()
        self.moves_by_colors = dict()
        self.update_possible_moves_by_colors()
        # we'll think of a better way to evaluate a turn in a board for the algorithm, but for now FIXME
        self.turn = Color.WHITE
        self.is_game_over = False

    def get_field_by_location(self, location) -> 'Field':
        '''Returns the field object at the given x, y location

        raises NonexistingFieldError if the given location is out of the 0-7 index bounds,
        which means no such field exists on the 8x8 board
        '''
        for field in self.one_dimensional_field_list:
            if field.location == location:
                return field
        raise NonexistingFieldCallError(f'Tried to obtain a nonexisting field: {location}')

    def _setup_fields(self):
        '''Fills the fields parameter with a correct setting of fields
        on a chessboard.
        '''
        self.fields = [[] for i in range(8)]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.fields[i].append(Field(BEIGE, i, j))
                else:
                    self.fields[i].append(Field(BROWN, i, j))

    def _setup_pieces(self):
        '''Sets up the pieces at the beginning of a game to their default positions
        '''
        for i in range(3):
            for j in range(8):
                current_field = self.fields[j][i]
                if current_field.color == BROWN:
                    piece = Piece(Color.BLACK, j, i)
                    current_field.piece = piece
                    # self.player_by_color(Color.BLACK).pieces.append(piece) FIXME

        for i in range(5, 8):
            for j in range(8):
                current_field = self.fields[j][i]
                if current_field.color == BROWN:
                    piece = Piece(Color.WHITE, j, i)
                    current_field.piece = piece
                    # self.player_by_color(Color.WHITE).pieces.append(piece) FIXME

    @property
    def fields(self):
        '''Getter for the fields parameter'''  # FIXME?
        return self._fields

    @fields.setter  # FIXME
    def fields(self, new_fields):
        '''Setter for the fields parameter'''
        self._fields = new_fields

    def __str__(self) -> str:
        #   to delete later, for testing purposes FIXME
        result = ''
        for row in self.fields:
            for field in row:
                if field.is_taken():
                    result += str(field.piece)
                else:
                    result += str(field)
            result += '\n'
        return result

    def delete_piece(self, piece):
        '''
        Remove a given piece from the board when it's jumped over.
        '''
        piece_field = self.get_field_by_location(piece.location)
        piece_field.piece = None
        self.pieces_by_colors[piece.color].remove(piece)
        del self.moves_by_colors[piece.color][piece]

    @property
    def one_dimensional_field_list(self):
        '''Returns the fields of the board in a list with length of 64
        so in most cases one for loop is used instead of 2 when iterating over them.'''
        field_list = list()
        for row in self.fields:
            for field in row:
                field_list.append(field)
        return field_list

    def setup_pieces_by_colors(self):
        '''Sets up the self.pieces_by_colors dictionary at the start of a game'''
        pieces_by_colors = {
            Color.WHITE: [],
            Color.BLACK: []
        }
        for field in self.one_dimensional_field_list:
            if field.is_taken():
                current_piece = field.piece
                pieces_by_colors[current_piece.color].append(current_piece)
        self.pieces_by_colors = pieces_by_colors

    def all_white_pieces(self):
        '''Returns a list of all white pieces in a game.'''
        return self.pieces_by_colors[Color.WHITE]

    def all_black_pieces(self):
        '''Returns a list of all black pieces in a game.'''
        return self.pieces_by_colors[Color.BLACK]

    def player_has_to_attack(self, color):  # MIGHT BE ABLE TO GET RID OF IT AND DO IT INSIDE OF UPDATE_MOVES FIXME
        '''Checks whether a player has to attack during the current round, returns a boolean'''
        player_dict = self.moves_by_colors[color]
        for value in player_dict.values():
            for move in value:
                if move.attacking:
                    return True
        return False

    def update_possible_moves_by_colors(self):
        '''Updates the possible_moves_by_colors parameter to reflect the current state of the board.
        '''
        moves_by_colors = {
            Color.WHITE: {},
            Color.BLACK: {}
        }

        for piece in self.all_white_pieces():
            moves_by_colors[Color.WHITE][piece] = piece.all_possible_legal_moves(self)
        for piece in self.all_black_pieces():
            moves_by_colors[Color.BLACK][piece] = piece.all_possible_legal_moves(self)

        self.moves_by_colors = moves_by_colors

        if self.player_has_to_attack(Color.WHITE):
            for piece in self.all_white_pieces():
                moves_by_colors[Color.WHITE][piece] = [move for move in piece.all_possible_legal_moves(self) if move.attacking]

        if self.player_has_to_attack(Color.BLACK):
            for piece in self.all_black_pieces():
                moves_by_colors[Color.BLACK][piece] = [move for move in piece.all_possible_legal_moves(self) if move.attacking]

        self.moves_by_colors = moves_by_colors

    def feasible_locations_and_moves_for_piece(self, piece):
        '''Returns the locations and moves a piece can move to in the current round'''
        self.update_possible_moves_by_colors()  # FIXME if we get set the has_to_attack inside of update, we don't have to run this one
        moves = self.moves_by_colors[piece.color][piece]
        locations = [move.new_cords for move in moves]
        return locations, moves

    def update_piece_location(self, piece, move):
        '''Moves the given piece by a given move inside of its and the fields'
        parameters'''
        piece.x, piece.y = move.new_cords
        self.get_field_by_location(move.old_cords).piece = None
        self.get_field_by_location(move.new_cords).piece = piece

    def can_piece_move(self, piece):  # MIGHT BE ABLE TO SIMPLIFY AFTER THE CHANGES ABOVE
        '''Determines whether a piece can be moved during a player's turn
        If the piece can't attack and another one of its color can,
        returns False. Else, returns True
        '''
        if self.player_has_to_attack(piece.color):
            if not piece.all_legal_attacking_moves(self):
                return False
        return True

    def get_jumped_piece(self, move):
        '''Returns a piece that gets jumped over during the given move so it can be removed'''
        old_x, old_y = move.old_cords
        next_x, next_y = move.new_cords
        jumped_x, jumped_y = int((old_x + next_x) / 2), int((old_y + next_y) / 2)
        piece = self.get_field_by_location((jumped_x, jumped_y)).piece
        return piece

    def handle_passive_move(self, move):
        '''Handles a passive move and its consequences including promotion,
        changing the turn etc.'''
        moving_piece = move.piece
        self.update_piece_location(moving_piece, move)
        if moving_piece.eligible_for_promotion_after_move(move) and not moving_piece.king:
            moving_piece.promote()
        self.change_turn()
        self.update_possible_moves_by_colors()
        if not self.player_has_moving_options(self.turn):
            self.is_game_over = True

    def handle_attacking_move(self, move):
        '''Handles an attacking move move and its consequences including promotion,
        changing the turn etc.'''
        moving_piece = move.piece
        jumped_piece = self.get_jumped_piece(move)
        self.delete_piece(jumped_piece)
        self.update_piece_location(moving_piece, move)
        if moving_piece.eligible_for_promotion_after_move(move) and not moving_piece.king:
            moving_piece.promote()
        self.update_possible_moves_by_colors()
        if not moving_piece.all_legal_attacking_moves(self):
            self.change_turn()
            if not self.player_has_moving_options(self.turn):
                self.is_game_over = True

    def handle_move(self, move):
        '''Compiles handle_attacking and passive move methods into one to simplify
        the code'''
        if move.attacking:
            self.handle_attacking_move(move)
        else:
            self.handle_passive_move(move)

    def all_possible_children_boards(self, color_to_move):
        '''Returns all possible boards that could derive from the possible moves
        of a player with a given color
        '''
        possible_boards = []
        for piece in self.moves_by_colors[color_to_move].keys():
            for move in self.moves_by_colors[color_to_move][piece]:
                temp_board = deepcopy(self)
                temp_piece = temp_board.get_field_by_location((piece.x, piece.y)).piece
                temp_move = Move(move.attacking, move.old_cords, move.new_cords, temp_piece)
                temp_board.handle_move(temp_move)
                possible_boards.append((temp_board, move))
        return possible_boards

    def evaluate_position(self):
        '''Evaluates the current situation on the board
        Positive evaluation means white has the edge, negative means
        black does. 0 Means the position is even. The methodology I used is described
        in the project's documentation'''
        if self.is_game_over:
            if self.winner() == Color.WHITE:
                return float('inf')
            elif self.winner() == Color.BLACK:
                return float('-inf')
        else:
            evaluation = 0
            # heuristics from http://www.cs.columbia.edu/~devans/TIC/AB.html FIXME
            sum_of_white_pieces = sum(piece.value for piece in self.all_white_pieces())
            sum_of_black_pieces = sum(piece.value for piece in self.all_black_pieces())
            evaluation += (sum_of_white_pieces - sum_of_black_pieces)

            # white_progression_list = [7 - piece.y for piece in self.all_white_pieces() if not piece.king]
            # average_progression_white = sum(white_progression_list) / len(white_progression_list) if white_progression_list else 0

            # black_progression_list = [piece.y for piece in self.all_black_pieces() if not piece.king]
            # average_progression_black = sum(black_progression_list) / len(black_progression_list) if black_progression_list else 0

            # evaluation += (average_progression_white - average_progression_black)

            # second_two_digits = average_progression_white - average_progression_black
            # if second_two_digits > 0:
            #     second_two_digits += 50 # any other way to

            #   to adjust later for a more exact evaluation
            return evaluation

    def player_has_moving_options(self, color):
        '''Checks whether a player with a given color has any possible moving options
        If he doesn't he lost the game.
        returns a boolean value'''
        player_dict = self.moves_by_colors[color]
        for value in player_dict.values():
            if len(value) > 0:
                return True
        return False

    def change_turn(self):
        '''Changes the turn parameter to the opposite color'''
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK

    def winner(self):
        '''Returns which player won the game or None if it's a tie'''
        if not self.player_has_moving_options(Color.BLACK):
            return Color.WHITE
        elif not self.player_has_moving_options(Color.WHITE):
            return Color.BLACK
        else:
            return None
