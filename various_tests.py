from checkers_ui import Ui_MainWindow
from PySide2.QtWidgets import QWidget
from PySide2 import QtCore
from board import Board
from field import Field
import typing


class FieldWidget(QWidget):
    def __init__(self, field: 'Field', parent: typing.Optional[QWidget] = ..., f: QtCore.Qt.WindowFlags = ...):
        super().__init__(parent, f)
        self._field = field


# board = Board
# def setup_pieces(board):
