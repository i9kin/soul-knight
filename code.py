import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel, QLCDNumber, QMessageBox, QCheckBox, QPlainTextEdit, QInputDialog, \
    QSpinBox, QVBoxLayout, QColorDialog
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
import math
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.polygon = 5

        self.color = QColor('red')
        self.size = 500
        self.k = 0.5

        self.n = 1
        
        self.resize(self.size, self.size)
        self.setWindowTitle('Рисование')
        self.k = 1 - self.k
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(self.color)
        self.drawFlag(qp)
        qp.end()

    def calc(self, a, b):
        return [(self.arr[a][0] + self.k * self.arr[b][0]) / (1 + self.k),
                (self.arr[a][1] + self.k * self.arr[b][1]) / (1 + self.k)]

    def top(self, a):
        r = self.size // 2
        x = 100 * math.cos((2 * math.pi * a + 45) / self.polygon)
        y = 100 * math.sin((2 * math.pi * a + 45) / self.polygon)
        return [r + x, r + y]

    def get_next(self):
        arr = []
        for i in range(self.polygon - 1):
            arr.append(self.calc(i, i + 1))
        arr.append(self.calc(self.polygon - 1, 0))
        self.arr = arr

    def drawFlag(self, qp):
        self.arr = [self.top(i) for i in range(self.polygon)]

        r = self.size // 2

        qp.drawLine(0, r, 500, r)


        qp.drawLine(r, 0, r, 500)


        for i in range(self.n):
            for i in range(self.polygon - 1):
                qp.drawLine(*self.arr[i], *self.arr[i + 1])
            qp.drawLine(*self.arr[-1], *self.arr[0])
            self.get_next()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
