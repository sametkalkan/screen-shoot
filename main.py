import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGraphicsScene, QGraphicsView, \
    QGraphicsItem, QMainWindow, QFileDialog, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen, QMouseEvent, QImage, QKeySequence, QCursor
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QRect
from PyQt5 import QtWidgets

from printscreen import PrintScreen

import keyboard



class App(QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.title = 'Screen Shot'

        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)

        self.setMinimumSize(50, 50)

        self.show()



def open_print_screen():
    print("open_print")
    img = QApplication.primaryScreen().grabWindow(0)
    PrintScreen(img)



if __name__ == '__main__':
    #keyboard.add_hotkey("alt+x", open_print_screen)

    app = QApplication(sys.argv)
    ex = App()
    #open_print_screen()
    # keyboard.wait('esc')
    sys.exit(app.exec_())















