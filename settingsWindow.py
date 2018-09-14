from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPolygon, QBrush
from PyQt5.QtWidgets import QWidget, QDesktopWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout


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

        self.setFixedSize(800, 490)
        self.center()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
