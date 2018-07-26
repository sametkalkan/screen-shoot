import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsItem, QMainWindow, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QImage, QKeySequence, QCursor
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QRect
from PyQt5 import QtWidgets


class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.title = 'Screen Shot'

        self.initUI()


    def initUI(self):

        self.setWindowTitle(self.title)

        self.setMinimumSize(600, 600)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
















