# from player import Player
from board import Board


class Game:

    def __init__(self, players) -> None:
        self._players = players
        self._board = Board()
        self._move_count_without_attacks = 0
        self.turn = self.player_by_color('white')
        self.result = None
        self.board._setup_fields()

    def player_by_color(self, color):
        player_color_dictionary = {
            player.color: player
            for player in self.players
        }
        return player_color_dictionary[color]


    @property
    def players(self):
        '''getter for the list of players in a game'''
        return self._players

    @property
    def moves_wo_attacks(self):
        '''getter for move_count_without_attacks
        when the move count reaches 50, the game ends in a draw
        the counter is reset to 0 with each attacking move made'''
        return self._move_count_without_attacks

    @property
    def board(self):
        return self._board
