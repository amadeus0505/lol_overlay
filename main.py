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
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QMouseEvent, QCloseEvent
import time
from pynput import keyboard
import handle_spotify


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.WIDTH = 500
        self.HEIGHT = 30
        self.transparancy_low = 0.5
        self.transparancy_high = 0.8
        self.resize(self.WIDTH, self.HEIGHT)
        self.move(150, 13)

        self.main_widget_rounded = QWidget(self)
        self.main_widget_rounded.resize(self.WIDTH, self.HEIGHT)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)
        self.not_clickable = True
        self.setWindowFlag(Qt.WindowTransparentForInput, self.not_clickable)

        radius = 10
        self.main_widget_rounded.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-radius:{0}px;
            """.format(radius)
        )

        self.main_layout = QHBoxLayout()

        self.label = QLabel("")
        self.label.setMinimumHeight(20)
        self.label.setMaximumWidth(int(self.WIDTH/3*2))
        self.label.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(self.label)

        self.btn_quit = QPushButton("Quit")
        self.btn_quit.clicked.connect(exit)
        self.main_layout.addWidget(self.btn_quit)

        self.main_widget_rounded.setLayout(self.main_layout)

        self.keyboard_listener = keyboard.Listener(on_press=self.keyPress)
        self.keyboard_listener.start()

        self.update_song = QTimer()
        self.update_song.setInterval(1000)
        self.update_song.timeout.connect(self.update_label)
        self.update_song.start()

        # offset to make window draggabel
        self.offset = None

    def enterEvent(self, a0: QEvent) -> None:
        opacity = self.transparancy_low
        while opacity < self.transparancy_high:
            opacity += 0.1
            self.setWindowOpacity(opacity)
            time.sleep(0.001)

    def leaveEvent(self, a0: QEvent) -> None:
        opacity = self.transparancy_high
        while opacity > self.transparancy_low:
            opacity -= 0.1
            self.setWindowOpacity(opacity)
            time.sleep(0.001)

    def keyPress(self, key):
        try:
            if key.char == "ß":
                print(self.not_clickable)
                self.not_clickable = not self.not_clickable
                self.setWindowFlag(Qt.WindowTransparentForInput, self.not_clickable)
        except AttributeError:
            pass

        print("before")
        self.show()
        print("showed")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.keyboard_listener.stop()
        event.accept()

    def update_label(self):
        name, artists = handle_spotify.get_current_track()
        self.label.setText(f"{name} - {', '.join(artists)}")

    # mouse press, move and releas event to make window draggable
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)


app = QApplication([])
window = MainWindow()
window.show()
exit(app.exec())
