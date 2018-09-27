import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
    QFileDialog, QColorDialog

from GUI.GeneralMainForm import GeneralMainForm
from PredictWindow import AppController
from SettingsWindow import SettingsWindow


class GeneralWindow(QMainWindow):
    def __init__(self, parent=None):
        super(GeneralWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(640, 480)
        self.setWindowTitle('Главное окно')
        #central_form = FormWidget()
        #self.setCentralWidget(central_form)
        self.show()


class FormWidget(QWidget):
    def __init__(self, parent=None):
        super(FormWidget, self).__init__(parent)
        self.ctrl = AppController(self)
        main_frame = GeneralMainForm()

        main_frame.duration_relax_line.ctrl.train_thread.set_time_relax(main_frame.duration_relax_line.text())
        main_frame.duration_relax_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_time_relax(main_frame.duration_relax_line.text()))

        main_frame.ctrl.train_thread.set_time_compress(main_frame.duration_compress_line.text())
        main_frame.duration_compress_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_time_compress(main_frame.duration_compress_line.text()))

        main_frame.ctrl.train_thread.set_number_repeats(main_frame.quantity_line.text())
        main_frame.quantity_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_number_repeats(main_frame.quantity_line.text()))

        main_frame.ctrl.train_thread.set_time_between_actions(main_frame.duration_compress_line.text())
        main_frame.duration_between_line.textChanged.connect(
            lambda: self.ctrl.train_thread.set_time_between_actions(main_frame.duration_between_line.text()))

        main_frame.icon_pack_button.clicked.connect(self.showDialog)
        main_frame.cpicker_button.clicked.connect(self.colorPicker)
        main_frame.train_button.clicked.connect(self.showTrainWindow)
        main_frame.online_button.clicked.connect(self.showPredictWindow)
        main_frame.settings_button.clicked.connect(self.showSettingsWindow)

        self.setLayout(main_frame)

    def showPredictWindow(self):
        pass

    def showTrainWindow(self):
        self.ctrl.train_mode()

    def showSettingsWindow(self):
        modal_settings_win = SettingsWindow(self)
        modal_settings_win.show()

    def showDialog(self):
        file = str(QFileDialog.getExistingDirectory(None, "Select Directory", "./src/themes"))
        self.ctrl.updatePixmaps(file)

    def colorPicker(self):
        color = QColorDialog.getColor()
        self.ctrl.setColorPalette(color.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GeneralWindow()
    sys.exit(app.exec_())

