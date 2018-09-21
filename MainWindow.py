import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, \
    QLabel, QLineEdit, QFileDialog, QColorDialog

from Control import Control
from settingsWindow import settingsWindow
from visualWindow import visualWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        centralForm = FormWidget()
        self.setCentralWidget(centralForm)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(640, 480)
        self.setWindowTitle('Главное окно')
        self.show()


class FormWidget(QWidget):
    def __init__(self, parent=None):
        super(FormWidget, self).__init__(parent)

        self.modalVisualWin = visualWindow(self)
        self.modalVisualWin.setHidden(True)

        duration_relax_label = QLabel("Продолжительность подсветки \"Отдыха\", сек ")
        duration_relax_line = QLineEdit()
        duration_relax_line.setText("2")
        duration_relax_hbox = QHBoxLayout()
        duration_relax_hbox.setSpacing(20)
        duration_relax_hbox.addWidget(duration_relax_label)
        duration_relax_hbox.addWidget(duration_relax_line)
        duration_relax_hbox.addStretch(1)

        duration_compress_label = QLabel("Продолжительность подсветки \"Сжатия\", сек  ")
        duration_compress_line = QLineEdit()
        duration_compress_line.setText("2")
        duration_compress_hbox = QHBoxLayout()
        duration_compress_hbox.setSpacing(20)
        duration_compress_hbox.addWidget(duration_compress_label)
        duration_compress_hbox.addWidget(duration_compress_line)
        duration_compress_hbox.addStretch(1)

        quantity_label = QLabel("Количество сжатий каждой руки                        ")
        quantity_line = QLineEdit()
        quantity_line.setText("5")
        quantity_hbox = QHBoxLayout()
        quantity_hbox.setSpacing(20)
        quantity_hbox.addWidget(quantity_label)
        quantity_hbox.addWidget(quantity_line)
        quantity_hbox.addStretch(1)

        icon_pack_label = QLabel("Директория с изображениями                        ")
        icon_pack_button = QPushButton("Выбрать папку")
        icon_pack_button.clicked.connect(self.showDialog)
        icon_pack_hbox = QHBoxLayout()
        icon_pack_hbox.setSpacing(20)
        icon_pack_hbox.addWidget(icon_pack_label)
        icon_pack_hbox.addWidget(icon_pack_button)
        icon_pack_hbox.addStretch(1)

        cpicker_label = QLabel("Цвет фона окна классификации                        ")
        cpicker_button = QPushButton("Выбрать цвет")
        cpicker_button.clicked.connect(self.colorPicker)
        cpicker_hbox = QHBoxLayout()
        cpicker_hbox.setSpacing(20)
        cpicker_hbox.addWidget(cpicker_label)
        cpicker_hbox.addWidget(cpicker_button)
        cpicker_hbox.addStretch(1)

        train_button = QPushButton("Обучить классификатор")
        train_button.clicked.connect(self.showTrainWindow)
        online_button = QPushButton("Онлайн режим")
        online_button.clicked.connect(self.showVisualWindow)
        settings_button = QPushButton("Настройки классификатора")
        settings_button.clicked.connect(self.showSettingsWindow)
        button_hbox = QHBoxLayout()
        button_hbox.setSpacing(15)
        button_hbox.addWidget(train_button)
        button_hbox.addWidget(online_button)
        button_hbox.addWidget(settings_button)
        button_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        vbox.addItem(duration_relax_hbox)
        vbox.addItem(duration_compress_hbox)
        vbox.addItem(quantity_hbox)
        vbox.addItem(icon_pack_hbox)
        vbox.addItem(cpicker_hbox)
        vbox.addItem(button_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def showVisualWindow(self):
        #self.modalVisualWin = visualWindow(self)
        self.modalVisualWin.centerMultiScreen()
        self.modalVisualWin.show()

    def showTrainWindow(self):
        pass

    def showSettingsWindow(self):
        modalSettingsWin = settingsWindow(self)
        modalSettingsWin.show()

    def showDialog(self):
        file = str(QFileDialog.getExistingDirectory(None, "Select Directory", "./src/themes"))
        self.modalVisualWin.updatePixmaps(file)

    def colorPicker(self):
        color = QColorDialog.getColor()
        self.modalVisualWin.setColorPallete(color.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
