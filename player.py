from random import randint
from piece_move_board import Piece, Board
from typing import List
from constants import FIELD_SIZE, MINIMAX_DEPTH


class Player:
    '''
    Class for representing a checkers player

    param color - the color of the player's pieces
    type color - str
    '''

    def __init__(self, color, ai=False) -> None:
        self.color = color
        self._ai = ai
        self._pieces = []

    @property
    def ai(self):
        '''
        Getter for the ai parameter
        when self.ai is true, the player is a bot,
        when it's false, the user controls the moves
        '''
        return self._ai

    @property
    def pieces(self):
        return self._pieces


class Bot(Player):
    def __init__(self, color, ai=True) -> None:
        super().__init__(color, ai)

    def click_random_piece(self, pieces: List[Piece]):  # maybe create a class variable to keep with the player and set it during the game?
        piece = pieces[randint(0, len(pieces) - 1)]
        piece_cords = (piece.x, piece.y)
        click_location = self.map_field_cords_to_pixels(piece_cords)
        return click_location

    def choose_random_possible_move_location(self, moves):
        field_to_move_cords = moves[randint(0, len(moves) - 1)].new_cords
        click_location = self.map_field_cords_to_pixels(field_to_move_cords)
        return click_location

    @staticmethod
    def map_field_cords_to_pixels(cords):
        x, y = cords
        return (x * FIELD_SIZE + 1 / 2 * FIELD_SIZE, y * FIELD_SIZE + 1 / 2 * FIELD_SIZE)


class MinimaxBot(Bot):
    def __init__(self, color, ai=True) -> None:
        super().__init__(color, ai)

    def minimax(self, board: 'Board', depth, original_move=None):
        maximizing_player = self.minimizing_or_maximizing(board.turn)

        if depth == 0 or board.is_game_over(board.turn):
            return (board.evaluate_position(), original_move)

        if maximizing_player:
            max_eval = (float('-inf'), None)
            for position, move in board.all_possible_children_boards(self.color):
                evaluation = self.minimax(position, depth - 1, move)
                if evaluation[0] > max_eval[0]:
                    max_eval = evaluation
                    best_move = move

            return max_eval[0], move

        else:
            min_eval = (float('inf'), None)
            for position, move in board.all_possible_children_boards(self.color):
                evaluation = self.minimax(position, depth - 1, move)
                if evaluation[0] < min_eval[0]:
                    min_eval = evaluation
                    best_move = move

            return min_eval[0], best_move

    @staticmethod
    def minimizing_or_maximizing(color):
        if color == 'white':
            return True
        return False

    def make_move(self, board):
        evaluation, move = self.minimax(board, MINIMAX_DEPTH)
        piece_click_location = self.map_field_cords_to_pixels(move.old_cords)
        field_click_location = self.map_field_cords_to_pixels(move.new_cords)
        print(evaluation)
        return piece_click_location, field_click_location
