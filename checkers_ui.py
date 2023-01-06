# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'checkers.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import images__rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(929, 912)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.board = QWidget(self.centralwidget)
        self.board.setObjectName(u"board")
        self.board.setEnabled(True)
        self.verticalLayout_2 = QVBoxLayout(self.board)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.field_14 = QWidget(self.board)
        self.field_14.setObjectName(u"field_14")
        self.field_14.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_14, 1, 5, 1, 1)

        self.field_53 = QWidget(self.board)
        self.field_53.setObjectName(u"field_53")
        self.field_53.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_53, 6, 4, 1, 1)

        self.field_8 = QWidget(self.board)
        self.field_8.setObjectName(u"field_8")
        self.field_8.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_8, 0, 7, 1, 1)

        self.field_11 = QWidget(self.board)
        self.field_11.setObjectName(u"field_11")
        self.field_11.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_11, 1, 2, 1, 1)

        self.field_25 = QWidget(self.board)
        self.field_25.setObjectName(u"field_25")
        self.field_25.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_25, 3, 0, 1, 1)

        self.field_54 = QWidget(self.board)
        self.field_54.setObjectName(u"field_54")
        self.field_54.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_54, 6, 5, 1, 1)

        self.field_40 = QWidget(self.board)
        self.field_40.setObjectName(u"field_40")
        self.field_40.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_40, 4, 7, 1, 1)

        self.field_12 = QWidget(self.board)
        self.field_12.setObjectName(u"field_12")
        self.field_12.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_12, 1, 3, 1, 1)

        self.field_24 = QWidget(self.board)
        self.field_24.setObjectName(u"field_24")
        self.field_24.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_24, 2, 7, 1, 1)

        self.field_47 = QWidget(self.board)
        self.field_47.setObjectName(u"field_47")
        self.field_47.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_47, 5, 6, 1, 1)

        self.field_18 = QWidget(self.board)
        self.field_18.setObjectName(u"field_18")
        self.field_18.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_18, 2, 1, 1, 1)

        self.field_27 = QWidget(self.board)
        self.field_27.setObjectName(u"field_27")
        self.field_27.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_27, 3, 2, 1, 1)

        self.field_57 = QWidget(self.board)
        self.field_57.setObjectName(u"field_57")
        self.field_57.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_57, 7, 0, 1, 1)

        self.field_42 = QWidget(self.board)
        self.field_42.setObjectName(u"field_42")
        self.field_42.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_42, 5, 1, 1, 1)

        self.field_33 = QWidget(self.board)
        self.field_33.setObjectName(u"field_33")
        self.field_33.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_33, 4, 0, 1, 1)

        self.field_4 = QWidget(self.board)
        self.field_4.setObjectName(u"field_4")
        self.field_4.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_4, 0, 3, 1, 1)

        self.field_52 = QWidget(self.board)
        self.field_52.setObjectName(u"field_52")
        self.field_52.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_52, 6, 3, 1, 1)

        self.field_17 = QWidget(self.board)
        self.field_17.setObjectName(u"field_17")
        self.field_17.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_17, 2, 0, 1, 1)

        self.field_58 = QWidget(self.board)
        self.field_58.setObjectName(u"field_58")
        self.field_58.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_58, 7, 1, 1, 1)

        self.field_3 = QWidget(self.board)
        self.field_3.setObjectName(u"field_3")
        self.field_3.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_3, 0, 2, 1, 1)

        self.field_31 = QWidget(self.board)
        self.field_31.setObjectName(u"field_31")
        self.field_31.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_31, 3, 6, 1, 1)

        self.field_29 = QWidget(self.board)
        self.field_29.setObjectName(u"field_29")
        self.field_29.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_29, 3, 4, 1, 1)

        self.field_39 = QWidget(self.board)
        self.field_39.setObjectName(u"field_39")
        self.field_39.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_39, 4, 6, 1, 1)

        self.field_36 = QWidget(self.board)
        self.field_36.setObjectName(u"field_36")
        self.field_36.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_36, 4, 3, 1, 1)

        self.field_20 = QWidget(self.board)
        self.field_20.setObjectName(u"field_20")
        self.field_20.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_20, 2, 3, 1, 1)

        self.field_32 = QWidget(self.board)
        self.field_32.setObjectName(u"field_32")
        self.field_32.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_32, 3, 7, 1, 1)

        self.field_56 = QWidget(self.board)
        self.field_56.setObjectName(u"field_56")
        self.field_56.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_56, 6, 7, 1, 1)

        self.field_15 = QWidget(self.board)
        self.field_15.setObjectName(u"field_15")
        self.field_15.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_15, 1, 6, 1, 1)

        self.field_16 = QWidget(self.board)
        self.field_16.setObjectName(u"field_16")
        self.field_16.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_16, 1, 7, 1, 1)

        self.field_49 = QWidget(self.board)
        self.field_49.setObjectName(u"field_49")
        self.field_49.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_49, 6, 0, 1, 1)

        self.field_41 = QWidget(self.board)
        self.field_41.setObjectName(u"field_41")
        self.field_41.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_41, 5, 0, 1, 1)

        self.field_10 = QWidget(self.board)
        self.field_10.setObjectName(u"field_10")
        self.field_10.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_10, 1, 1, 1, 1)

        self.field_48 = QWidget(self.board)
        self.field_48.setObjectName(u"field_48")
        self.field_48.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_48, 5, 7, 1, 1)

        self.field_64 = QWidget(self.board)
        self.field_64.setObjectName(u"field_64")
        self.field_64.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_64, 7, 7, 1, 1)

        self.field_43 = QWidget(self.board)
        self.field_43.setObjectName(u"field_43")
        self.field_43.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_43, 5, 2, 1, 1)

        self.field_44 = QWidget(self.board)
        self.field_44.setObjectName(u"field_44")
        self.field_44.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_44, 5, 3, 1, 1)

        self.field_38 = QWidget(self.board)
        self.field_38.setObjectName(u"field_38")
        self.field_38.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_38, 4, 5, 1, 1)

        self.field_61 = QWidget(self.board)
        self.field_61.setObjectName(u"field_61")
        self.field_61.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_61, 7, 4, 1, 1)

        self.field_63 = QWidget(self.board)
        self.field_63.setObjectName(u"field_63")
        self.field_63.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_63, 7, 6, 1, 1)

        self.field_35 = QWidget(self.board)
        self.field_35.setObjectName(u"field_35")
        self.field_35.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_35, 4, 2, 1, 1)

        self.field_51 = QWidget(self.board)
        self.field_51.setObjectName(u"field_51")
        self.field_51.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_51, 6, 2, 1, 1)

        self.field_2 = QWidget(self.board)
        self.field_2.setObjectName(u"field_2")
        self.field_2.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_2, 0, 1, 1, 1)

        self.field_59 = QWidget(self.board)
        self.field_59.setObjectName(u"field_59")
        self.field_59.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_59, 7, 2, 1, 1)

        self.field_5 = QWidget(self.board)
        self.field_5.setObjectName(u"field_5")
        self.field_5.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_5, 0, 4, 1, 1)

        self.field_23 = QWidget(self.board)
        self.field_23.setObjectName(u"field_23")
        self.field_23.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_23, 2, 6, 1, 1)

        self.field_34 = QWidget(self.board)
        self.field_34.setObjectName(u"field_34")
        self.field_34.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_34, 4, 1, 1, 1)

        self.field_19 = QWidget(self.board)
        self.field_19.setObjectName(u"field_19")
        self.field_19.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_19, 2, 2, 1, 1)

        self.field_30 = QWidget(self.board)
        self.field_30.setObjectName(u"field_30")
        self.field_30.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_30, 3, 5, 1, 1)

        self.field_50 = QWidget(self.board)
        self.field_50.setObjectName(u"field_50")
        self.field_50.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_50, 6, 1, 1, 1)

        self.field_13 = QWidget(self.board)
        self.field_13.setObjectName(u"field_13")
        self.field_13.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_13, 1, 4, 1, 1)

        self.field_7 = QWidget(self.board)
        self.field_7.setObjectName(u"field_7")
        self.field_7.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_7, 0, 6, 1, 1)

        self.field_46 = QWidget(self.board)
        self.field_46.setObjectName(u"field_46")
        self.field_46.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_46, 5, 5, 1, 1)

        self.field_55 = QWidget(self.board)
        self.field_55.setObjectName(u"field_55")
        self.field_55.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_55, 6, 6, 1, 1)

        self.field_37 = QWidget(self.board)
        self.field_37.setObjectName(u"field_37")
        self.field_37.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_37, 4, 4, 1, 1)

        self.field_28 = QWidget(self.board)
        self.field_28.setObjectName(u"field_28")
        self.field_28.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_28, 3, 3, 1, 1)

        self.field_60 = QWidget(self.board)
        self.field_60.setObjectName(u"field_60")
        self.field_60.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_60, 7, 3, 1, 1)

        self.field_22 = QWidget(self.board)
        self.field_22.setObjectName(u"field_22")
        self.field_22.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_22, 2, 5, 1, 1)

        self.field_1 = QWidget(self.board)
        self.field_1.setObjectName(u"field_1")
        self.field_1.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_1, 0, 0, 1, 1)

        self.field_9 = QWidget(self.board)
        self.field_9.setObjectName(u"field_9")
        self.field_9.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_9, 1, 0, 1, 1)

        self.field_62 = QWidget(self.board)
        self.field_62.setObjectName(u"field_62")
        self.field_62.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_62, 7, 5, 1, 1)

        self.field_21 = QWidget(self.board)
        self.field_21.setObjectName(u"field_21")
        self.field_21.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_21, 2, 4, 1, 1)

        self.field_26 = QWidget(self.board)
        self.field_26.setObjectName(u"field_26")
        self.field_26.setStyleSheet(u"background-color: rgb(255, 254, 242);")

        self.gridLayout.addWidget(self.field_26, 3, 1, 1, 1)

        self.field_45 = QWidget(self.board)
        self.field_45.setObjectName(u"field_45")
        self.field_45.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_45, 5, 4, 1, 1)

        self.field_6 = QWidget(self.board)
        self.field_6.setObjectName(u"field_6")
        self.field_6.setStyleSheet(u"background-color: rgb(139, 69, 19);")

        self.gridLayout.addWidget(self.field_6, 0, 5, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.board)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 929, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

