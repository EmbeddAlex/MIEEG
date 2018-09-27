import random
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QDesktopWidget, QApplication

import confParser


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
        confParser.config_file.read("paths", "theme_path")
        if (directory is not None) & (directory != ""):
            confParser.config_file.write("paths", "theme_path", directory)

        theme_path = confParser.config_file.read("paths", "theme_path")
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

    def change_arrow(self, arrow, state):
        if arrow == 'right':
            if state == 'first':
                self.rightArrow.setPixmap(self.rightArrowFirst)
            if state == 'second':
                self.rightArrow.setPixmap(self.rightArrowSecond)
        if arrow == 'center':
            if state == 'first':
                self.centerRelax.setPixmap(self.centerRelaxFirst)
            if state == 'second':
                self.centerRelax.setPixmap(self.centerRelaxSecond)
        if arrow == 'left':
            if state == 'first':
                self.leftArrow.setPixmap(self.leftArrowFirst)
            if state == 'second':
                self.leftArrow.setPixmap(self.leftArrowSecond)


class VisualWindow(QWidget):
    def __init__(self, parent=None):
        super(VisualWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowTitle("Application")
        self.arrowsSet = Arrows()
        self.initUI()

    def initUI(self):
        self.setLayout(self.arrowsSet)
        self.setColorPalette(confParser.config_file.read("color", "bg_color"))
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
        mouse_pointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mouse_pointer_position)
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
        confParser.config_file.write("color", "bg_color", current_bg_color)
        background_color = QColor()
        background_color.setNamedColor(current_bg_color)
        p = self.palette()
        p.setColor(self.backgroundRole(), background_color)
        self.setPalette(p)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


class AppController(VisualWindow):
    def __init__(self, parent=None):
        super(AppController, self).__init__(parent)
        self.train_thread = TrainThread()
        self.train_thread.signal_stimul_action.connect(self.arrowsSet.change_arrow)

    def train_mode(self):
        self.centerMultiScreen()
        self.show()
        self.train_thread.start()

    def visual_mode(self):
        pass


class TrainThread(QThread):
    signal_stimul_action = pyqtSignal(str, str)

    time_relax_val = 0
    time_compress_val = 0
    number_repeats_val = 0
    time_between_val = 0

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.generate_random_sequence(self.number_repeats_val)

    def set_number_repeats(self, num):
        if num is not "":
            self.number_repeats_val = int(num)
        else:
            self.number_repeats_val = 1

    def set_time_compress(self, time_sec):
        if time_sec is not "":
            self.time_compress_val = int(time_sec)
        else:
            self.time_compress_val = 1

    def set_time_relax(self, time_sec):
        if time_sec is not "":
            self.time_relax_val = int(time_sec)
        else:
            self.time_relax_val = 1

    def set_time_between_actions(self, time_sec):
        if time_sec is not "":
            self.time_between_val = int(time_sec)
        else:
            self.time_between_val = 1

    def generate_random_sequence(self, quantity):
        arrow_array = []
        i = 0

        while i < quantity:
            arrow_array.append('left')
            arrow_array.append('right')
            i += 1
        random.shuffle(arrow_array)
        print(arrow_array)

        time.sleep(self.time_between_val)
        self.signal_stimul_action.emit('center', 'second')
        time.sleep(self.time_relax_val)
        self.signal_stimul_action.emit('center', 'first')
        time.sleep(self.time_between_val)

        for arrow in arrow_array:
            self.signal_stimul_action.emit(arrow, 'second')
            time.sleep(self.time_compress_val)
            self.signal_stimul_action.emit(arrow, 'first')
            time.sleep(self.time_between_val)
            self.signal_stimul_action.emit('center', 'second')
            time.sleep(self.time_relax_val)
            self.signal_stimul_action.emit('center', 'first')
            time.sleep(self.time_between_val)
