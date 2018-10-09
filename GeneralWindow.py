import sys

from IPython.core.tests.test_debugger import can_exit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, \
    QLabel, QLineEdit, QFileDialog, QColorDialog

import confParser
from PredictWindow import AppController
from SettingsWindow import settingsWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        central_form = FormWidget()
        self.setCentralWidget(central_form)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(640, 480)
        self.setWindowTitle('Main window')
        self.show()


class FormWidget(QWidget):

    def __init__(self, parent=None):
        super(FormWidget, self).__init__(parent)
        self.ctrl = AppController()

        self.duration_relax_line = QLineEdit()
        self.duration_compress_line = QLineEdit()
        self.quantity_line = QLineEdit()
        self.duration_between_line = QLineEdit()

        self.icon_pack_button = QPushButton("Выбрать папку")
        self.cpicker_button = QPushButton("Выбрать цвет")
        self.train_button = QPushButton("Обучить классификатор")
        self.online_button = QPushButton("Онлайн режим")
        self.settings_button = QPushButton("Настройки классификатора")

        self.UI_init()

    def UI_init(self):
        duration_relax_label = QLabel("Продолжительность подсветки \"Отдыха\", сек ")
        self.duration_relax_line.setText(str(confParser.config_file.read("parameters", "relax_time")))
        self.duration_relax_line.setValidator(QRegExpValidator(QRegExp('[0-9]{1,20}')))
        self.ctrl.train_thread.set_time_relax(self.duration_relax_line.text())
        self.duration_relax_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_time_relax(self.duration_relax_line.text()))
        duration_relax_hbox = QHBoxLayout()
        duration_relax_hbox.setSpacing(20)
        duration_relax_hbox.addWidget(duration_relax_label)
        duration_relax_hbox.addWidget(self.duration_relax_line)
        duration_relax_hbox.addStretch(1)

        duration_compress_label = QLabel("Продолжительность подсветки \"Сжатия\", сек  ")
        self.duration_compress_line.setText(str(confParser.config_file.read("parameters", "compress_time")))
        self.duration_compress_line.setValidator(QRegExpValidator(QRegExp('[0-9]{1,20}')))
        self.ctrl.train_thread.set_time_compress(self.duration_compress_line.text())
        self.duration_compress_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_time_compress(self.duration_compress_line.text()))
        duration_compress_hbox = QHBoxLayout()
        duration_compress_hbox.setSpacing(20)
        duration_compress_hbox.addWidget(duration_compress_label)
        duration_compress_hbox.addWidget(self.duration_compress_line)
        duration_compress_hbox.addStretch(1)

        quantity_label = QLabel("Количество сжатий каждой руки                        ")
        self.quantity_line.setText(str(confParser.config_file.read("parameters", "quantity_compressions")))
        self.quantity_line.setValidator(QRegExpValidator(QRegExp('[0-9]{1,20}')))
        self.ctrl.train_thread.set_number_repeats(self.quantity_line.text())
        self.quantity_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_number_repeats(self.quantity_line.text()))
        quantity_hbox = QHBoxLayout()
        quantity_hbox.setSpacing(20)
        quantity_hbox.addWidget(quantity_label)
        quantity_hbox.addWidget(self.quantity_line)
        quantity_hbox.addStretch(1)

        duration_between_label = QLabel("Пауза между стимулами, сек                                ")
        self.duration_between_line.setText(str(confParser.config_file.read("parameters", "between_time")))
        self.duration_between_line.setValidator(QRegExpValidator(QRegExp('[0-9]{1,20}')))
        self.ctrl.train_thread.set_time_between_actions(self.duration_compress_line.text())
        self.duration_between_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_time_between_actions(self.duration_between_line.text()))
        duration_between_hbox = QHBoxLayout()
        duration_between_hbox.setSpacing(20)
        duration_between_hbox.addWidget(duration_between_label)
        duration_between_hbox.addWidget(self.duration_between_line)
        duration_between_hbox.addStretch(1)

        icon_pack_label = QLabel("Директория с изображениями                             ")
        icon_pack_hbox = QHBoxLayout()
        icon_pack_hbox.setSpacing(20)
        icon_pack_hbox.addWidget(icon_pack_label)
        icon_pack_hbox.addWidget(self.icon_pack_button)
        icon_pack_hbox.addStretch(1)

        cpicker_label = QLabel("Цвет фона окна классификации                         ")
        cpicker_hbox = QHBoxLayout()
        cpicker_hbox.setSpacing(20)
        cpicker_hbox.addWidget(cpicker_label)
        cpicker_hbox.addWidget(self.cpicker_button)
        cpicker_hbox.addStretch(1)

        self.train_button.clicked.connect(self.showTrainWindow)
        self.online_button.clicked.connect(self.showPredictWindow)
        self.settings_button.clicked.connect(self.showSettingsWindow)
        self.icon_pack_button.clicked.connect(self.showDialog)
        self.cpicker_button.clicked.connect(self.colorPicker)

        button_hbox = QHBoxLayout()
        button_hbox.setSpacing(15)
        button_hbox.addWidget(self.train_button)
        button_hbox.addWidget(self.online_button)
        button_hbox.addWidget(self.settings_button)
        button_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        vbox.addItem(duration_relax_hbox)
        vbox.addItem(duration_compress_hbox)
        vbox.addItem(duration_between_hbox)
        vbox.addItem(quantity_hbox)
        vbox.addItem(icon_pack_hbox)
        vbox.addItem(cpicker_hbox)
        vbox.addItem(button_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def showPredictWindow(self):
        pass

    def showTrainWindow(self):
        self.ctrl.train_mode()

    def showSettingsWindow(self):
        modal_settings_win = settingsWindow(self)
        modal_settings_win.show()

    def showDialog(self):
        file = str(QFileDialog.getExistingDirectory(None, "Select Directory", "./src/themes"))
        if file is not "":
            confParser.config_file.write("paths", "theme_path", str(file))

    def colorPicker(self):
        color = QColorDialog.getColor()
        self.ctrl.setColorPalette(color.name())

    def closeEvent(self, event):
        if can_exit:
            self.ctrl.close()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
