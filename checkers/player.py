from random import randint, shuffle
from checkers.piece_move_board import Piece, Board
from typing import List
from checkers.constants import FIELD_SIZE, Color
from time import time


class Player:
    '''
    Class representing a checkers player

    param color - the color of the player's pieces
    type color - Color

    param ai - whether the player is controlled by the computer
    type ai - bool
    '''

    def __init__(self, color, ai=False) -> None:
        self.color = color
        self._ai = ai

    @property
    def ai(self):
        '''
        Getter for the ai parameter
        '''
        return self._ai


class Bot(Player):
    def __init__(self, color, ai=True) -> None:
        super().__init__(color, ai)

    @staticmethod
    def map_field_cords_to_pixels(cords):
        x, y = cords
        return (x * FIELD_SIZE + 1 / 2 * FIELD_SIZE,
                y * FIELD_SIZE + 1 / 2 * FIELD_SIZE)


class RandomBot(Bot):

    def __init__(self, color) -> None:
        super().__init__(color, ai=True)

    def click_random_piece(self, pieces: List[Piece]):
        piece = pieces[randint(0, len(pieces) - 1)]
        piece_cords = (piece.x, piece.y)
        click_location = self.map_field_cords_to_pixels(piece_cords)
        return click_location

    def choose_random_possible_move_location(self, moves):
        field_to_move_cords = moves[randint(0, len(moves) - 1)].new_cords
        click_location = self.map_field_cords_to_pixels(field_to_move_cords)
        return click_location


class MinimaxBot(Bot):
    '''
    Class representing a bot using the minimax algorithm
    to make a move

    param color: color of the bot's pieces
    type color: Color

    param depth: the depth of the evaluating algorithm
    type depth: int in range(1, 11)
    '''

    def __init__(self, color, depth, time_limit) -> None:
        super().__init__(color, ai=True)
        self._depth = depth
        self._time_limit = time_limit

    def minimax(self, board: 'Board', depth, alpha=float('-inf'),
                beta=float('inf'), original_move=None):
        '''
        The function used to determine which move is the best for the bot
        param: type
        board: Board
        depth: int
        alpha: float
        beta: float
        original_move: Move or None by default in the first call made

        returns:
        board evaluation: int
        best_move/original_move: Move
        '''
        maximizing_player = self.minimizing_or_maximizing(board.turn)

        if depth == 0 or board.is_game_over:
            return (board.evaluate_position(), original_move)

        best_move = None
        if maximizing_player:
            max_eval = (float('-inf'), None)
            possible_children = board.all_possible_children_boards(board.turn)
            if len(possible_children) == 1:
                only_child = possible_children[0]
                only_board = only_child[0]
                only_move = only_child[1]
                return only_board.evaluate_position(), only_move

            else:
                for position, move in possible_children:
                    evaluation = self.minimax(
                        position, depth - 1, alpha, beta, move)
                    if evaluation[0] == max_eval[0] and best_move is None:
                        max_eval = evaluation
                        best_move = move
                    elif evaluation[0] > max_eval[0]:
                        max_eval = evaluation
                        best_move = move
                    alpha = max(alpha, evaluation[0])
                    if beta <= alpha:
                        break

                return max_eval[0], best_move

        else:
            min_eval = (float('inf'), None)
            possible_children = board.all_possible_children_boards(board.turn)

            if len(possible_children) == 1:
                only_child = possible_children[0]
                only_board = only_child[0]
                only_move = only_child[1]
                return only_board.evaluate_position(), only_move

            shuffle(possible_children)
            #   to make the game non deterministic in positions with
            #   no clear winning/advantageous move
            for position, move in possible_children:
                evaluation = self.minimax(
                    position, depth - 1, alpha, beta, move)
                if evaluation[0] == min_eval[0] and best_move is None:
                    min_eval = evaluation
                    best_move = move
                elif evaluation[0] < min_eval[0]:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation[0])
                if beta <= alpha:
                    break
            return min_eval[0], best_move

    @ staticmethod
    def minimizing_or_maximizing(color):
        '''
        Returns whether the player of a given color aims
        to maximize or minimize the evaluation in a position
        white = maximizing - returns True
        black = minimizing - returns False
        '''
        if color == Color.WHITE:
            return True
        return False

    def make_move(self, board):
        '''
        The method responsible for the entire process of making a move:
        calculation and mapping the move into the pixel grid of the window.
        '''
        if not self.time_limit:
            current_move = self.minimax(board, self.depth)[1]

        else:
            current_depth = 0
            current_move = self.minimax(board, 1)[1]
            start_time = time()
            time_left = self.time_limit - (time() - start_time)

            while time_left >= 0.3 * self.time_limit:
                # if the time left is less than 0.3 of the max limit,
                # increasing the depth would pretty much double current
                # time spent on the move, so we need to limit it this way

                current_depth += 1
                if current_depth > self.depth:
                    break
                current_move = self.minimax(board, current_depth)[1]
                time_left = self.time_limit - (time() - start_time)

        piece_click_location = self.map_field_cords_to_pixels(
            current_move.old_cords)
        field_click_location = self.map_field_cords_to_pixels(
            current_move.new_cords)

        return piece_click_location, field_click_location

    @property
    def depth(self):
        '''Getter for the depth attribute'''
        return self._depth

    @property
    def time_limit(self):
        '''Getter for the time_limit attribute'''
        return self._time_limit
