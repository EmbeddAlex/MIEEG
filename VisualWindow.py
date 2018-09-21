import time
from threading import Thread

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
        config_file = ConfParser("src/settings.conf")
        config_file.read("paths", "theme_path")
        if (directory is not None) & (directory != ""):
            config_file.write("paths", "theme_path", directory)

        theme_path = config_file.read("paths", "theme_path")
        print(theme_path)
        self.leftArrowFirst = QPixmap(theme_path + "./first_l.png")
        self.centerRelaxFirst = QPixmap(theme_path + "./first_relax.png")
        self.rightArrowFirst = QPixmap(theme_path + "./first_r.png")

        self.leftArrowSecond = QPixmap(theme_path + "./second_l.png")
        self.centerRelaxSecond = QPixmap(theme_path + "./second_relax.png")
        self.rightArrowSecond = QPixmap(theme_path + "./second_r.png")

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


class VisualWindow(QWidget):
    configFile = ConfParser("src/settings.conf")

    def __init__(self, parent=None):
        super(VisualWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowTitle("Application")
        self.arrowsSet = Arrows()
        self.initUI()

    def initUI(self):
        self.setLayout(self.arrowsSet)
        self.setColorPalette(self.configFile.read("color", "bg_color"))
        self.showFullScreen()
        self.setHidden(True)
        number_available_desktops = QDesktopWidget().screenCount()
        if number_available_desktops > 1:
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
            center_point = QApplication.desktop().screenGeometry(1).center()
        elif screen == 1:
            window_geometry = QRect(QApplication.desktop().screenGeometry(0))
            self.resize(window_geometry.width(), window_geometry.height())
            center_point = QApplication.desktop().screenGeometry(0).center()
        else:
            window_geometry = self.frameGeometry()
            center_point = QDesktopWidget.availableGeometry().center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def setColorPalette(self, current_bg_color):
        self.configFile.write("color", "bg_color", current_bg_color)
        background_color = QColor()
        background_color.setNamedColor(current_bg_color)
        p = self.palette()
        p.setColor(self.backgroundRole(), background_color)
        self.setPalette(p)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_G:
            self.arrowsSet.rightArrowIsSecond()
        if e.key() == Qt.Key_S:
            self.arrowsSet.rightArrowIsFirst()


class Controller(VisualWindow):
    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.mythread = MyThread("First")

    def train_mode(self):
        self.show()
        self.mythread.start()
        #self.close()

    def visual_mode(self):
        pass


class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        time.sleep(2)
        #rightArrowIsSecond()
        print("Thread complete")
