from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPolygon, QBrush
from PyQt5.QtWidgets import QWidget, QDesktopWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QApplication


class settingsWindow(QWidget):
    def __init__(self, parent=None):
        super(settingsWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Модальное окно")
        self.initUI()

    def initUI(self):

        greyButton = QPushButton("Grey")
        blueButton = QPushButton("Blue")
        greenButton = QPushButton("Green")
        hbox = QHBoxLayout()
        hbox.addWidget(greyButton)
        hbox.addWidget(blueButton)
        hbox.addWidget(greenButton)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        #self.setFixedSize(800, 490)
        self.center2()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def center2(self):
        window_geometry = self.frameGeometry()
        mousepointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mousepointer_position)
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        window_geometry.moveCenter(centerPoint)
        self.move(window_geometry.topLeft())

    def center3(self):
        window_geometry = QRect(QApplication.desktop().screenGeometry(1))
        self.resize(window_geometry.width(), window_geometry.height())
        centerPoint = QApplication.desktop().screenGeometry(1).center()
        window_geometry.moveCenter(centerPoint)
        self.move(window_geometry.topLeft())
