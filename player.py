from random import randint
from piece_move_board import Piece
from typing import List
from constants import FIELD_SIZE


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
