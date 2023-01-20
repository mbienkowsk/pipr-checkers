from checkers.constants import BEIGE, Placeholder

from checkers.field import Field


def test_init():
    field1 = Field(BEIGE, 0, 0)
    assert not field1.piece
    assert field1.x == 0
    assert field1.y == 0
    assert field1.color == BEIGE
    assert not field1.is_taken()


def test_is_taken():
    field1 = Field(BEIGE, 0, 0)
    assert not field1.is_taken()
    field1.piece = Placeholder.PIECE
    assert field1.is_taken()


def test_location():
    field1 = Field(BEIGE, 0, 0)
    assert field1.location == (0, 0)
