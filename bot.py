class Bot:
    def __init__(self, color: str, moves: dict) -> None:
        self.color = color
        self._moves = moves


    @property
    def moves(self):
        moves = []
        for value in self._moves.values():
            for move in value:
                moves.append(move)

        return moves


