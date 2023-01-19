
class Field:
    '''
    Class representing a single field on the checkerboard.

    param color: the color of the field
    type color: tup(int) (an rgb value)

    param piece: the piece currently on the field
    type piece: Piece or None if no piece is on the field

    param x: the field's column's index
    type x: int

    param y: the field's row's index
    type y: int
    '''

    def __init__(self, color, x, y) -> None:
        self.color = color
        self._piece = None
        self._x = x
        self._y = y

    def is_taken(self):
        '''Returns True if the field is occupied by a piece, else False'''
        if self.piece is None:
            return False
        return True

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
        '''Returns the x and y coordinates of a field in a tuple'''
        return (self.x, self.y)

    def __str__(self) -> str:  # FIXME
        return f'[{self.location}]'

    @property
    def piece(self):
        '''Getter for the piece attribute'''
        return self._piece

    @piece.setter
    def piece(self, new_piece):
        '''Setter for the piece attribute'''
        self._piece = new_piece
