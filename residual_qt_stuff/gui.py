from PySide2.QtWidgets import QMainWindow, QApplication, QGridLayout, QLabel, QVBoxLayout
from PySide2.QtGui import QPixmap
from checkers_ui import Ui_MainWindow
import sys
from board import Board
from piece import Piece


class CheckersWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def guiMain(args):
    app = QApplication(args)
    window = CheckersWindow()
    board = Board()

    setup_board_to_gui_connection(board, window.ui.field_layout)
    draw_pawns(board, window.ui.field_layout)
    setup_pawns(board)
    field_widget = board.get_field_by_location((1, 2)).corresponding_widget
    field_widget.setStyleSheet(u"background-color: rgb(255, 105, 180);")

    window.show()
    return app.exec_()


def setup_board_to_gui_connection(board: 'Board', grid_layout: 'QGridLayout'):

    for i in range(8):
        for j in range(8):
            field_widget = grid_layout.itemAtPosition(j, i).widget()
            field_object = board.get_field_by_location((i, j))
            field_object.corresponding_widget = field_widget


def draw_pawns(board: 'Board', grid_layout: 'QGridLayout'):
    for row in board.fields:
        for field in row:
            if field.is_taken:
                piece = field.piece
                widget = grid_layout.itemAtPosition(field.y, field.x).widget()

                field_layout = QVBoxLayout()
                field_layout.addWidget(widget)

                piece_label = QLabel(widget)
                if piece.color == 'white':
                    piece_pixmap = QPixmap('images/white_piece.png')
                else:
                    piece_pixmap = QPixmap('images/black_piece.png')
                piece_label.setPixmap(piece_pixmap)


def setup_pawns(board):
    for i in range(3):
        for j in range(8):
            current_field = board.fields[i][j]
            if current_field.color == 'black':
                piece = Piece('black', i, j)
                current_field.piece = piece
                # self.player_by_color('black').pieces.append(piece)

    for i in range(5, 8):
        for j in range(8):
            current_field = board.fields[i][j]
            if current_field.color == 'black':
                piece = Piece('white', i, j)
                current_field.piece = piece
                # self.player_by_color('white').pieces.append(piece)


if __name__ == '__main__':
    guiMain(sys.argv)
