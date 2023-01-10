

class Field:
    def __init__(self, color, x, y) -> None:
        self.color = color
        self._piece = None
        self._x = x
        self._y = y
        self._corresponding_widget = None

    def is_taken(self):
        if self.piece is None:
            return False
        return True

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
        return f'[{self.color}, {self.location}]'

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, new_piece):
        self._piece = new_piece
