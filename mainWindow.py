import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QAction

from modalWindow import modalWindow


class mainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        exitAction = QAction('&Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        modalAction = QAction('Start', self)
        modalAction.setStatusTip('Start learning')
        modalAction.triggered.connect(self.showModalWindow)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(modalAction)
        fileMenu.addAction(exitAction)

        self.statusBar().showMessage('Ready')
        self.setMinimumSize(840, 480)
        self.setWindowTitle('Главное окно')
        self.show()

    def showModalWindow(self):
        print("Окно открыто")
        modalWin = modalWindow(self)
        modalWin.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
