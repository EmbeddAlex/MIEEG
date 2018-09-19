from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QColor, QPalette
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QDesktopWidget, QApplication

from confParser import ConfParser


class arrows(QHBoxLayout):
    def __init__(self, parent=None):
        super(arrows, self).__init__(parent)
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
        if directory is not None:
            print(configFile.conf.sections())
            configFile.write("paths", "theme_path", directory)

        themePath = configFile.read("paths", "theme_path")

        self.leftArrowFirst = QPixmap(themePath + "first_l.png")
        self.centerRelaxFirst = QPixmap(themePath + "first_relax.png")
        self.rightArrowFirst = QPixmap(themePath + "first_r.png")

        self.leftArrowSecond = QPixmap(themePath + "second_l.png")
        self.centerRelaxSecond = QPixmap(themePath + "second_relax.png")
        self.rightArrowSecond = QPixmap(themePath + "second_r.png")

        self.leftArrow.setPixmap(self.leftArrowFirst)
        self.centerRelax.setPixmap(self.centerRelaxFirst)
        self.rightArrow.setPixmap(self.rightArrowFirst)

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
        #self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Модальное окно")
        self.initUI()

    def initUI(self):
        self.arrowsSet = arrows()
        self.setLayout(self.arrowsSet)
        self.configFile = ConfParser("src/settings.conf")
        colorRead = self.configFile.read("color", "bg_color")
        self.setColorPallete(colorRead)
        self.showFullScreen()
        numberAvailableDesktops = QDesktopWidget().screenCount()
        if numberAvailableDesktops > 1:
            self.centerMultuScreen()
        else:
            self.centerSingleScreen()

    def updatePixmaps(self, directory):
        self.arrowsSet.setPixmaps(directory)

    def centerSingleScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def centerMultuScreen(self):
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
        if e.key() == Qt.Key_G:
            self.arrowsSet.leftArrowIsGreen()
            self.arrowsSet.centerRelaxIsGreen()
            self.arrowsSet.rightArrowIsGreen()
        if e.key() == Qt.Key_S:
            self.arrowsSet.leftArrowIsGray()
            self.arrowsSet.centerRelaxIsGray()
            self.arrowsSet.rightArrowIsGray()
