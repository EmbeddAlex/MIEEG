from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QDesktopWidget, QApplication

from confParser import ConfParser


class Arrows(QHBoxLayout):
    def __init__(self, parent=None):
        super(Arrows, self).__init__(parent)
        self.setSpacing(40)

        self.leftArrow = QLabel()
        self.centerRelax = QLabel()
        self.rightArrow = QLabel()
        self.setPixmaps(None)

        self.addStretch(1)
        self.addWidget(self.leftArrow)
        self.addWidget(self.centerRelax)
        self.addWidget(self.rightArrow)
        self.addStretch(1)

    def setPixmaps(self, directory):
        configFile = ConfParser("src/settings.conf")
        configFile.read("paths", "theme_path")
        if (directory is not None) & (directory != ""):
            configFile.write("paths", "theme_path", directory)

        themePath = configFile.read("paths", "theme_path")
        print(themePath)
        self.leftArrowFirst = QPixmap(themePath + "./first_l.png")
        self.centerRelaxFirst = QPixmap(themePath + "./first_relax.png")
        self.rightArrowFirst = QPixmap(themePath + "./first_r.png")

        self.leftArrowSecond = QPixmap(themePath + "./second_l.png")
        self.centerRelaxSecond = QPixmap(themePath + "./second_relax.png")
        self.rightArrowSecond = QPixmap(themePath + "./second_r.png")

        self.leftArrow.setPixmap(self.leftArrowFirst)
        self.centerRelax.setPixmap(self.centerRelaxFirst)
        self.rightArrow.setPixmap(self.rightArrowFirst)

    def rightArrowIsFirst(self):
        self.rightArrow.setPixmap(self.rightArrowFirst)

    def rightArrowIsSecond(self):
        self.rightArrow.setPixmap(self.rightArrowSecond)

    def centerRelaxIsFirst(self):
        self.centerRelax.setPixmap(self.centerRelaxFirst)

    def centerRelaxIsSecond(self):
        self.centerRelax.setPixmap(self.centerRelaxSecond)

    def leftArrowIsFirst(self):
        self.leftArrow.setPixmap(self.leftArrowFirst)

    def leftArrowIsSecond(self):
        self.leftArrow.setPixmap(self.leftArrowSecond)


class visualWindow(QWidget):
    def __init__(self, parent=None):
        super(visualWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowTitle("Модальное окно")
        self.initUI()

    def initUI(self):
        self.arrowsSet = Arrows()
        self.setLayout(self.arrowsSet)
        self.configFile = ConfParser("src/settings.conf")
        colorRead = self.configFile.read("color", "bg_color")
        self.setColorPallete(colorRead)
        self.showFullScreen()
        numberAvailableDesktops = QDesktopWidget().screenCount()
        if numberAvailableDesktops > 1:
            self.centerMultiScreen()
        else:
            self.centerSingleScreen()

    def updatePixmaps(self, directory):
        self.arrowsSet.setPixmaps(directory)

    def centerSingleScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def centerMultiScreen(self):
        mousepointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mousepointer_position)
        if screen == 0:
            window_geometry = QRect(QApplication.desktop().screenGeometry(1))
            self.resize(window_geometry.width(), window_geometry.height())
            centerPoint = QApplication.desktop().screenGeometry(1).center()
        elif screen == 1:
            window_geometry = QRect(QApplication.desktop().screenGeometry(0))
            self.resize(window_geometry.width(), window_geometry.height())
            centerPoint = QApplication.desktop().screenGeometry(0).center()
        else:
            window_geometry = self.frameGeometry()
            centerPoint = QDesktopWidget.availableGeometry().center()
        window_geometry.moveCenter(centerPoint)
        self.move(window_geometry.topLeft())

    def setColorPallete(self, currentBGColor):
        self.configFile.write("color", "bg_color", currentBGColor)
        background_color = QColor()
        background_color.setNamedColor(currentBGColor)
        p = self.palette()
        p.setColor(self.backgroundRole(), background_color)
        self.setPalette(p)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
