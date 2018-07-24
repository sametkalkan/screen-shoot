import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsItem, QMainWindow, QFileDialog, QVBoxLayout, QMenu
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QImage, QContextMenuEvent
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QRect
from PyQt5 import QtWidgets


class SelectableObject(QWidget):
    def __init__(self, parent=None, pixmap=None):
        print("SELECTABLE init---")
        super(SelectableObject, self).__init__()

        self.setAttribute(Qt.WA_StaticContents)

        self.label = QLabel(parent)
        self.picture = pixmap

        self.label.setPixmap(self.picture)
        self.label.resize(self.label.sizeHint())


        self.beginX = None
        self.beginY = None

        self.draw = False

        self.currentX = None
        self.currentY = None

        self.pen = QPen(Qt.green, 2, Qt.SolidLine)
        self.brush = QBrush(Qt.green)

        self.update()

    def paintEvent(self, QPaintEvent):

        if self.draw:
            painter = QPainter(self)
            painter.setPen(QPen(self.pen))
            painter.drawRect(self.beginX, self.beginY, self.currentX - self.beginX, self.currentY - self.beginY)

            painter.drawRect(self.label.x(), self.label.y(), self.label.width(), self.label.height())

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
        self.lastX = e.x()
        self.lastY = e.y()
        pass

    def save(self):
        cropped = self.picture.copy(self.beginX, self.beginY, self.lastX - self.beginX, self.lastY - self.beginY)
        cropped.save("cpy.jpg")

    def clearThis(self):
        print("clear this selectable")
        self.draw = False
        self.update()

    def contextMenuEvent(self, e: QContextMenuEvent):
        contextMenu = QMenu(self)

        save = contextMenu.addAction("save")

        action = contextMenu.exec_(self.mapToGlobal(e.pos()))

        if action == save:
            self.save()

class PrintScreen(QMainWindow):

    def __init__(self, parent, pixmap):
        super(PrintScreen, self).__init__(parent)

        self.title = 'PrintScreen'

        self.s = SelectableObject(self, pixmap)
        self.setCentralWidget(self.s)

        self.setWindowTitle(self.title)
        self.showFullScreen()
        #self.setMinimumSize(1300, 1024)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e: QMouseEvent):
        print(e.pos())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PrintScreen(QPixmap("2.jpg"))
    sys.exit(app.exec_())
















