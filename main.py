import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsItem, QMainWindow, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QImage
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QRect
from PyQt5 import QtWidgets


class SelectableObject(QWidget):
    def __init__(self, parent=None, pixmap=None):
        print("SELECTABLE init---")
        super(SelectableObject, self).__init__()

        self.setAttribute(Qt.WA_StaticContents)

        self.par = parent
        self.l = QLabel(parent)
        self.p = pixmap

        self.l.setPixmap(self.p)
        self.l.resize(self.l.sizeHint())


        self.beginX = None
        self.beginY = None

        self.draw = False

        self.currentX = None
        self.currentY = None

        self.pen = QPen(Qt.black, 5, Qt.SolidLine)
        self.brush = None

        self.update()

    def get_to_be_saved_pic(self, pixmap):
        self.l.setPixmap(pixmap)

    def set_pixmap(self, pixmap):
        self.l.setPixmap(pixmap)

    def setPen(self, pen):
        self.pen = pen

    def setBrush(self, brush):
        self.brush = brush

    def paintEvent(self, QPaintEvent):

        if self.draw:
            painter = QPainter(self)
            painter.setPen(QPen(self.pen))
            painter.drawRect(self.beginX, self.beginY, self.currentX - self.beginX, self.currentY - self.beginY)

            painter.drawRect(self.l.x(), self.l.y(), self.l.width(), self.l.height())

    def mousePressEvent(self, e: QMouseEvent):
        if e.button()==Qt.LeftButton:
            self.draw = True
            self.beginX = e.x()
            self.beginY = e.y()

            self.currentX = e.x()
            self.currentY = e.y()

            self.update()

    def mouseMoveEvent(self, e: QMouseEvent):
        self.currentX = e.x()
        self.currentY = e.y()
        self.update()

    def mouseReleaseEvent(self, e: QMouseEvent):
        cropped = self.p.copy(self.beginX, self.beginY, e.x()-self.beginX, e.y()-self.beginY)
        cropped.save("cpy.jpg")


    def clearThis(self):
        print("clear this selectable")
        self.draw = False
        self.update()




class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.title = 'Rectangle'
        self.initUI()


    def initUI(self):
        # pixmap = QPixmap("3.jpg")
        # self.l = Label(self, pixmap)

        bttn = QPushButton("Clear", self)
        bttn.setGeometry(200, 600, 100, 50)

        bttn.clicked.connect(self.clearThis)



        self.setWindowTitle(self.title)
        #self.showFullScreen()
        self.setMinimumSize(1300, 1024)
        self.show()


    def clearThis(self):
        self.s = SelectableObject(self, QPixmap("2.jpg"))
        self.setCentralWidget(self.s)
        self.s.l.setPixmap(QPixmap("2.jpg"))
        self.s.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Enter:
            self.s = SelectableObject(self, QPixmap("2.jpg"))
            self.setCentralWidget(self.s)


class Button(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setText("Push")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
















