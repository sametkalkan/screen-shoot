import io
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsItem, QMainWindow, QFileDialog, QVBoxLayout, QMenu
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QImage, QContextMenuEvent, QColor, QCursor
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QRect, QBuffer, QByteArray, QDate, QTime
from PyQt5 import QtWidgets

from PIL import Image
import win32clipboard
from io import BytesIO
import os

def to_clipboard(pixmap):
    pixmap.save("temp.jpg")
    img = QImage("temp.jpg")
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    img.save(buffer, "JPG")
    img = Image.open(io.BytesIO(buffer.data()))
    ##img = Image.open("2.jpg")
    output = BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    os.remove("temp.jpg")

class SelectableObject(QWidget):
    def __init__(self, parent=None, pixmap=None):
        print("SELECTABLE init---")
        super(SelectableObject, self).__init__()

        self.parent = parent

        self.setAttribute(Qt.WA_StaticContents)

        self.label = QLabel(parent)
        self.picture = pixmap


        self.label.setPixmap(self.picture)
        self.label.resize(self.label.sizeHint())

        self.drawRectangle = False
        self.drawLine = True

        self.beginX = None
        self.beginY = None

        self.currentX = None
        self.currentY = None

        self.selectedArea = QRect()

        self.update()

    def paintEvent(self, QPaintEvent):

        if self.drawRectangle:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
            self.selectedArea.setCoords(self.beginX, self.beginY, self.currentX, self.currentY)
            painter.fillRect(self.selectedArea, QBrush(QColor(128, 128, 255, 128)))
            painter.drawRect(self.beginX, self.beginY, self.currentX - self.beginX, self.currentY - self.beginY)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button()==Qt.LeftButton:
            self.drawRectangle = True
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
        if e.button() == Qt.LeftButton:
            if self.currentX<self.beginX:
                tmp = self.beginX
                self.beginX = self.currentX
                self.currentX = tmp
            if self.currentY<self.beginY:
                tmp = self.beginY
                self.beginY = self.currentY
                self.currentY = tmp

            self.selectedArea.setCoords(self.beginX, self.beginY, self.currentX, self.currentY)

    def save(self):
        cropped = self.picture.copy(self.selectedArea)
        date = QDate.currentDate().toString("dd-MM-yyyy")
        time = QTime().currentTime().toString("hh-mm-ss")
        img_name = date + "_" + time + ".jpg"
        fileName = QFileDialog.getSaveFileName(self, 'Save File', img_name, "Image Format (*.jpg)")
        cropped.save(fileName[0])

    def to_clipboard(self):
        cropped = self.picture.copy(self.selectedArea)
        to_clipboard(pixmap=cropped)

    def contextMenuEvent(self, e: QContextMenuEvent):
        contextMenu = QMenu(self)

        save = contextMenu.addAction("Save")
        to_clipboard = contextMenu.addAction("Copy to clipboard")
        save_and_buffer = contextMenu.addAction("Save and Buffer")
        contextMenu.addSeparator()
        exit = contextMenu.addAction("Exit")

        action = contextMenu.exec_(self.mapToGlobal(e.pos()))

        if action == save:
            self.save()
            self.parent.close_screen()
        elif action == to_clipboard:
            self.to_clipboard()
            self.parent.close_screen()
        elif action == save_and_buffer:
            self.save()
            self.to_clipboard()
            self.parent.close_screen()
        elif action == exit:
            self.parent.close_screen()


class PrintScreen(QMainWindow):

    def __init__(self, parent, pixmap):
        super(PrintScreen, self).__init__(parent)

        self.setCursor(QCursor(Qt.CrossCursor)) # changes the cursor to cross(plus sign)

        self.title = 'PrintScreen'

        self.s = SelectableObject(self, pixmap)
        self.setCentralWidget(self.s)

        self.setWindowTitle(self.title)
        self.showFullScreen()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, e):
        self.close()
        pass

    def mouseMoveEvent(self, e: QMouseEvent):
        print("move")
        print(e.pos())

    def close_screen(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    img = QApplication.primaryScreen().grabWindow(0)
    to_clipboard(img)
    PrintScreen(None, img)

    sys.exit(app.exec_())
















