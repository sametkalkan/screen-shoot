import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsItem, QMainWindow, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QImage, QKeySequence, QCursor
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QRect
from PyQt5 import QtWidgets

from printscreen import PrintScreen

class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.title = 'Rectangle'

        self.initUI()


    def initUI(self):

        # pixmap = QPixmap("3.jpg")
        # self.l = Label(self, pixmap)

        self.setWindowTitle(self.title)
        #self.showFullScreen()
        self.setMinimumSize(600, 600)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter:
            p = QApplication.primaryScreen().grabWindow(0)
            #self.open(QPixmap("2.jpg"))
            self.open(p)

    def open(self, pixmap):
        ex = PrintScreen(self, pixmap)
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
















