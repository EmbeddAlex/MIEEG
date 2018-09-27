from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QPolygon, QBrush
from PyQt5.QtWidgets import QWidget, QDesktopWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QApplication


class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Настройки классификатора")
        self.initUI()

    def initUI(self):

        grey_button = QPushButton("Кнопка 1")
        blue_button = QPushButton("Кнопка 2")
        green_button = QPushButton("Кнопка 3")
        hbox = QHBoxLayout()
        hbox.addWidget(grey_button)
        hbox.addWidget(blue_button)
        hbox.addWidget(green_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
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
