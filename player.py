from random import randint
from piece_move_board import Piece
from typing import List


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

    def choose_random_piece_location(pieces: List[Piece]):  # maybe create a class variable to keep with the player and set it during the game?
        piece = pieces[randint(0, len(pieces) - 1)]
        return piece.x, piece.y

    # choose_random_possible_move()
