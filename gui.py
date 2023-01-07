from PySide2.QtWidgets import QMainWindow, QApplication, QGridLayout
from checkers_ui import Ui_MainWindow
import sys
from board import Board


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


if __name__ == '__main__':
    guiMain(sys.argv)
