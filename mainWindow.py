import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, \
    QLabel, QLineEdit, QFileDialog

from settingsWindow import settingsWindow
from trainWindow import TrainWindow
from visualWindow import visualWindow


class mainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        centralForm = FormWidget()
        self.setCentralWidget(centralForm)
        self.statusBar().showMessage('Ready')
        self.setMinimumSize(840, 480)
        self.setWindowTitle('Главное окно')
        self.show()


class FormWidget(QWidget):
    def __init__(self, parent=None):
        super(FormWidget, self).__init__(parent)

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
        vbox.addItem(button_hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def showVisualWindow(self):
        modalVisualWin = visualWindow(self)
        modalVisualWin.show()

    def showTrainWindow(self):
        modalTrainWin = TrainWindow(self)
        modalTrainWin.show()

    def showSettingsWindow(self):
        modalSettingsWin = settingsWindow(self)
        modalSettingsWin.show()

    def showDialog(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
