# import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    app = QApplication(sys.argv)
    # definiujemy instancje aplikacji,
    # argv to pomocnicza zmienna dla interpretera

    win = QMainWindow()
    # definiujemy okno aplikacji

    win.setGeometry(0, 0, 300, 300)
    # ustawiamy od lewej pozycje x i y naszego okna na ekranie
    # oraz jego wymiary

    win.setWindowTitle('Sysy sie sknyszyl!')
    # tytul aplkikacji - wyswietla sie na pasku z gory po lewej

    win.show()
    # bez tego nie pokaze sie w ogole to okno

    sys.exit(app.exec_())
    # zapewniamy smooth exit aplikacji whatever that means
    # po prostu kiedy metoda exec (klikniecie x) sie wydarzy,
    # system zamyka proces


window()
