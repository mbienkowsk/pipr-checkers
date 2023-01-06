class Field:
    def __init__(self, color, x, y) -> None:
        self.color = color
        self.piece = None
        self._x = x
        self._y = y

    def is_taken(self):
        if not self.piece:
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