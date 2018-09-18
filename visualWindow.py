from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QDesktopWidget, qApp, QApplication
from sympy import true


class arrows(QHBoxLayout):
    def __init__(self, parent=None):
        super(arrows, self).__init__(parent)
        self.setSpacing(40)

        self.leftArrowFirst = QPixmap("src/themes/green/grey_l.png")
        self.centerRelaxFirst = QPixmap("src/themes/green/grey_relax.png")
        self.rightArrowFirst = QPixmap("src/themes/green/grey_r.png")

        self.leftArrowSecond = QPixmap("src/themes/green/green_l.png")
        self.centerRelaxSecond = QPixmap("src/themes/green/green_relax.png")
        self.rightArrowSecond = QPixmap("src/themes/green/green_r.png")

        self.leftArrow = QLabel()
        self.leftArrow.setPixmap(self.leftArrowFirst)
        self.centerRelax = QLabel()
        self.centerRelax.setPixmap(self.centerRelaxFirst)
        self.rightArrow = QLabel()
        self.rightArrow.setPixmap(self.rightArrowFirst)

        self.addStretch(1)
        self.addWidget(self.leftArrow)
        self.addWidget(self.centerRelax)
        self.addWidget(self.rightArrow)
        self.addStretch(1)


    def rightArrowIsGray(self):
        self.rightArrow.setPixmap(self.rightArrowFirst)

    def rightArrowIsGreen(self):
        self.rightArrow.setPixmap(self.rightArrowSecond)

    def centerRelaxIsGray(self):
        self.centerRelax.setPixmap(self.centerRelaxFirst)

    def centerRelaxIsGreen(self):
        self.centerRelax.setPixmap(self.centerRelaxSecond)

    def leftArrowIsGray(self):
        self.leftArrow.setPixmap(self.leftArrowFirst)

    def leftArrowIsGreen(self):
        self.leftArrow.setPixmap(self.leftArrowSecond)


class visualWindow(QWidget):

    def __init__(self, parent=None):
        super(visualWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Модальное окно")
        self.initUI()

    def initUI(self):
        self.arrowsSet = arrows()
        self.setLayout(self.arrowsSet)
        self.checks('#00557f')
        self.showFullScreen()
        self.center3()

    def center(self):
        pass

    def center3(self):
        window_geometry = QRect(QApplication.desktop().screenGeometry(1))
        self.resize(window_geometry.width(), window_geometry.height())
        centerPoint = QApplication.desktop().screenGeometry(1).center()
        window_geometry.moveCenter(centerPoint)
        self.move(window_geometry.topLeft())

    def setBGColor(self, bg):
        self.checks(bg)
        print(bg)

    def checks(self, currentBGColor):
        self.background_color = QColor()
        self.background_color.setNamedColor(currentBGColor)
        p = self.palette()
        p.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(p)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_G:
            self.arrowsSet.leftArrowIsGreen()
            self.arrowsSet.centerRelaxIsGreen()
            self.arrowsSet.rightArrowIsGreen()
        if e.key() == Qt.Key_S:
            self.arrowsSet.leftArrowIsGray()
            self.arrowsSet.centerRelaxIsGray()
            self.arrowsSet.rightArrowIsGray()
