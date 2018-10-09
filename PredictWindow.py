import random
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QDesktopWidget, QApplication

import confParser


class Arrows(QHBoxLayout):
    height_k = 1
    width_k = 1

    def __init__(self, parent=None):
        super(Arrows, self).__init__(parent)

        theme_path = confParser.config_file.read("paths", "theme_path")
        self.centerRelaxSecond = QPixmap(theme_path + "./second_relax.png")
        self.leftArrowSecond = QPixmap(theme_path + "./second_l.png")
        self.rightArrowFirst = QPixmap(theme_path + "./first_r.png")
        self.rightArrowSecond = QPixmap(theme_path + "./second_r.png")
        self.centerRelaxFirst = QPixmap(theme_path + "./first_relax.png")
        self.leftArrowFirst = QPixmap(theme_path + "./first_l.png")
        #self.setSpacing(20)

        self.leftArrow = QLabel()
        self.leftArrow.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.centerRelax = QLabel()
        self.centerRelax.setAlignment(Qt.AlignBottom)
        self.rightArrow = QLabel()
        self.rightArrow.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        self.addStretch(1)
        self.addWidget(self.leftArrow)
        self.addWidget(self.centerRelax)
        self.addWidget(self.rightArrow)
        self.addStretch(1)

    def change_arrow(self, arrow, state):
        if arrow == 'right':
            if state == 'first':
                self.rightArrow.setPixmap(self.rightArrowFirst.scaled(self.rightArrowFirst.width()*self.width_k,
                                                                      self.rightArrowFirst.height()*self.height_k,
                                                                      Qt.KeepAspectRatio, Qt.SmoothTransformation))
            if state == 'second':
                self.rightArrow.setPixmap(self.rightArrowSecond.scaled(self.rightArrowSecond.width()*self.width_k,
                                                                       self.rightArrowSecond.height()*self.height_k,
                                                                       Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if arrow == 'center':
            if state == 'first':
                self.centerRelax.setPixmap(self.centerRelaxFirst.scaled(self.centerRelaxFirst.width()*self.width_k,
                                                                        self.centerRelaxFirst.height()*self.height_k,
                                                                        Qt.KeepAspectRatio, Qt.SmoothTransformation))
            if state == 'second':
                self.centerRelax.setPixmap(self.centerRelaxSecond.scaled(self.centerRelaxSecond.width()*self.width_k,
                                                                         self.centerRelaxSecond.height()*self.height_k,
                                                                         Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if arrow == 'left':
            if state == 'first':
                self.leftArrow.setPixmap(self.leftArrowFirst.scaled(self.leftArrowFirst.width()*self.width_k,
                                                                    self.leftArrowFirst.height()*self.height_k,
                                                                    Qt.KeepAspectRatio, Qt.SmoothTransformation))
            if state == 'second':
                self.leftArrow.setPixmap(self.leftArrowSecond.scaled(self.leftArrowSecond.width()*self.width_k,
                                                                     self.leftArrowSecond.height()*self.height_k,
                                                                     Qt.KeepAspectRatio, Qt.SmoothTransformation))


class VisualWindow(QWidget):
    def __init__(self, parent=None):
        super(VisualWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.arrowsSet = Arrows()
        self.initUI()

    def initUI(self):
        self.setLayout(self.arrowsSet)
        self.setColorPalette(confParser.config_file.read("color", "bg_color"))
        self.setHidden(True)

    def find_available_desktops(self):
        number_available_desktops = QDesktopWidget().screenCount()
        if number_available_desktops > 1:
            self.centerMultiScreen()
        else:
            self.centerSingleScreen()

    def centerSingleScreen(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def centerMultiScreen(self):
        mouse_pointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mouse_pointer_position)
        print("current screen " + str(screen))

        self.window_one = QRect(QApplication.desktop().screenGeometry(0))
        self.window_two = QRect(QApplication.desktop().screenGeometry(1))

        if screen == 0:
            window_geometry = QRect(QApplication.desktop().screenGeometry(1))
            self.resize(window_geometry.width(), window_geometry.height())
            center_point = QApplication.desktop().screenGeometry(1).center()
            self.arrowsSet.height_k = (self.window_two.height() / self.window_one.height())
            self.arrowsSet.width_k = (self.window_two.width() / self.window_one.width())
        elif screen == 1:
            window_geometry = QRect(QApplication.desktop().screenGeometry(0))
            self.resize(window_geometry.width(), window_geometry.height())
            center_point = QApplication.desktop().screenGeometry(0).center()
            self.arrowsSet.height_k = (self.window_one.height() / self.window_two.height())
            self.arrowsSet.width_k = (self.window_one.width() / self.window_two.width())
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


class AppController(VisualWindow):
    def __init__(self, parent=None):
        super(AppController, self).__init__(parent)
        self.train_thread = MyThread()
        self.train_thread.signal_stimulus_action.connect(self.arrowsSet.change_arrow)

    def train_mode(self):
        self.find_available_desktops()
        self.set_default_arrows()
        self.train_thread.delay_allow_sem = True
        self.train_thread.start()
        self.showFullScreen()
        self.find_available_desktops()

    def predict_mode(self):
        pass

    def set_default_arrows(self):
        self.arrowsSet.change_arrow('left', 'first')
        self.arrowsSet.change_arrow('center', 'first')
        self.arrowsSet.change_arrow('right', 'first')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
            self.train_thread.delay_allow_sem = False


class MyThread(QThread):
    signal_stimulus_action = pyqtSignal(str, str)

    time_relax_val = 0
    time_compress_val = 0
    number_repeats_val = 0
    time_between_val = 0
    delay_allow_sem = True

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        self.generate_random_sequence(self.number_repeats_val)

    def set_number_repeats(self, num):
        if num is not "":
            self.number_repeats_val = int(num)
            confParser.config_file.write("parameters", "quantity_compressions", str(num))

    def set_time_compress(self, time_sec):
        if time_sec is not "":
            self.time_compress_val = int(time_sec)
            confParser.config_file.write("parameters", "compress_time", str(time_sec))

    def set_time_relax(self, time_sec):
        if time_sec is not "":
            self.time_relax_val = int(time_sec)
            confParser.config_file.write("parameters", "relax_time", str(time_sec))

    def set_time_between_actions(self, time_sec):
        if time_sec is not "":
            self.time_between_val = int(time_sec)
            confParser.config_file.write("parameters", "between_time", str(time_sec))

    def generate_random_sequence(self, quantity):
        arrow_array = []
        i = 0

        while i < quantity:
            arrow_array.append('left')
            arrow_array.append('right')
            i += 1
        random.shuffle(arrow_array)
        print(arrow_array)

        self.delay_sec(self.time_between_val)
        self.signal_stimulus_action.emit('center', 'second')
        self.delay_sec(self.time_relax_val)
        self.signal_stimulus_action.emit('center', 'first')
        self.delay_sec(self.time_between_val)

        for arrow in arrow_array:
            self.signal_stimulus_action.emit(arrow, 'second')
            self.delay_sec(self.time_compress_val)
            self.signal_stimulus_action.emit(arrow, 'first')
            self.delay_sec(self.time_between_val)
            self.signal_stimulus_action.emit('center', 'second')
            self.delay_sec(self.time_relax_val)
            self.signal_stimulus_action.emit('center', 'first')
            self.delay_sec(self.time_between_val)

        print("Thread finished")

    def delay_sec(self, sec):
        if self.delay_allow_sem:
            sec = sec * 100
            while sec > 0:
                sec = sec - 10
                time.sleep(0.1)
                if not self.delay_allow_sem:
                    break
