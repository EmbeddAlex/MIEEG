from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QPolygon, QBrush
from PyQt5.QtWidgets import QWidget, QDesktopWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout


class ShapesWidget(QWidget):
    color = Qt.green

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(1, 30)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawWidget(painter)
        painter.end()

    def drawWidget(self, qp):
        qp.setPen(QPen(Qt.darkGreen, 2, Qt.SolidLine))
        qp.setBrush(QBrush(self.color, Qt.SolidPattern))
        points = QPolygon([QPoint(50, 200), QPoint(250, 100), QPoint(250, 300)])
        qp.drawPolygon(points)
        points = QPolygon([QPoint(750, 200), QPoint(550, 100), QPoint(550, 300)])
        qp.drawPolygon(points)
        qp.drawEllipse(325, 125, 150, 150)

    def setColor(self, currentColor):
        self.color = currentColor
        self.repaint()


class TrainWindow(QWidget):
    def __init__(self, parent=None):
        super(TrainWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle("Модальное окно")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.initUI()

    def initUI(self):
        shape = ShapesWidget()

        greyButton = QPushButton("Grey")
        blueButton = QPushButton("Blue")
        greenButton = QPushButton("Green")
        blueButton.clicked.connect(lambda: shape.setColor(Qt.blue))
        greenButton.clicked.connect(lambda: shape.setColor(Qt.green))
        greyButton.clicked.connect(lambda: shape.setColor(Qt.gray))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(greyButton)
        hbox.addWidget(blueButton)
        hbox.addWidget(greenButton)

        vbox = QVBoxLayout()
        vbox.addWidget(shape)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setFixedSize(800, 490)
        #self.showFullScreen()
        self.center()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

