

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
