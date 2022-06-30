from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMouseEvent
import time
from pynput import keyboard


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.WIDTH = 300
        self.HEIGHT = 300
        self.resize(self.WIDTH, self.HEIGHT)

        self.main_widget_rounded = QWidget(self)
        self.main_widget_rounded.resize(self.WIDTH, self.HEIGHT)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.clickable = True
        self.setWindowOpacity(0.5)

        radius = 30
        self.main_widget_rounded.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-radius:{0}px;
            """.format(radius)
        )

        self.main_layout = QHBoxLayout()

        self.label = QLabel("Test")
        self.main_layout.addWidget(self.label)

        self.btn_quit = QPushButton("Quit")
        self.btn_quit.clicked.connect(self.close)
        self.main_layout.addWidget(self.btn_quit)

        self.main_widget_rounded.setLayout(self.main_layout)

        self.setWindowFlag(Qt.WindowTransparentForInput, True)

        self.listener = keyboard.Listener(on_press=self.keyPress)
        self.listener.start()

    def enterEvent(self, a0: QEvent) -> None:
        opacity = 0.50
        while opacity < 0.90:
            opacity += 0.1
            self.setWindowOpacity(opacity)
            time.sleep(0.001)

    def leaveEvent(self, a0: QEvent) -> None:
        opacity = 0.90
        while opacity > 0.50:
            opacity -= 0.1
            self.setWindowOpacity(opacity)
            time.sleep(0.001)

    def keyPress(self, key):
        try:
            if key.char == "ß":
                self.clickable = not self.clickable
                self.setWindowFlag(Qt.WindowTransparentForInput, self.clickable)
                self.show()
        except AttributeError:
            pass


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
