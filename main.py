from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QMainWindow
)
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QCloseEvent, QFont, QIcon
import time
from pynput import keyboard
import handle_spotify
from icon_button import IconButton


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.WIDTH = 500
        self.HEIGHT = 30
        self.transparancy_low = 0.6
        self.transparancy_high = 0.8
        self.resize(self.WIDTH, self.HEIGHT)
        self.move(150, 13)

        self.main_widget_rounded = QWidget(self)
        self.main_widget_rounded.resize(self.WIDTH, self.HEIGHT)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(self.transparancy_low)
        self.not_clickable = True
        self.setWindowFlag(Qt.WindowTransparentForInput, self.not_clickable)

        radius = 5
        self.main_widget_rounded.setStyleSheet(
            """
            background:rgb(255, 255, 255);
            border-radius:{0}px;
            """.format(radius)
        )

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.lbl_songinfo = QLabel()
        self.lbl_songinfo.setFixedHeight(30)
        self.lbl_songinfo.setFont(QFont('Times', 10, QFont.Bold))
        self.lbl_songinfo.setFixedWidth(int(self.WIDTH / 3 * 2))
        self.lbl_songinfo.setContentsMargins(10, 0, 0, 0)
        self.main_layout.addWidget(self.lbl_songinfo, alignment=Qt.AlignCenter)

        self.control_layout = QHBoxLayout()
        self.control_layout.setAlignment(Qt.AlignHCenter)

        self.btn_back = IconButton()
        self.btn_back.setIcon(QIcon("icons/back.png"))
        self.btn_back.clicked.connect(self.back)
        self.control_layout.addWidget(self.btn_back)

        self.btn_pause = IconButton()

        if handle_spotify.is_currently_playing():
            self.btn_pause.setIcon(QIcon("icons/pause.png"))
        else:
            self.btn_pause.setIcon(QIcon("icons/play.png"))

        self.btn_pause.clicked.connect(self.toggle)
        self.control_layout.addWidget(self.btn_pause)

        self.btn_forward = IconButton()
        self.btn_forward.setIcon(QIcon("icons/forward.png"))
        self.btn_forward.clicked.connect(self.forward)
        self.control_layout.addWidget(self.btn_forward)

        self.main_layout.addLayout(self.control_layout)

        self.btn_quit = IconButton()
        self.btn_quit.setIcon(QIcon("icons/exit.png"))
        self.btn_quit.clicked.connect(exit)
        self.main_layout.addWidget(self.btn_quit)

        self.main_widget_rounded.setLayout(self.main_layout)

        self.keyboard_listener = keyboard.Listener(on_press=self.keyPress)
        self.keyboard_listener.start()

        self.update_song = QTimer()
        self.update_song.setInterval(1000)
        self.update_song.timeout.connect(self.update_label)
        self.update_song.start()

    def enterEvent(self, a0: QEvent) -> None:
        self.setWindowOpacity(self.transparancy_high)
        super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.setWindowOpacity(self.transparancy_low)
        super().leaveEvent(a0)

    def keyPress(self, key):
        try:
            if key.char == "ß":
                self.not_clickable = not self.not_clickable
                self.setWindowFlag(Qt.WindowTransparentForInput, self.not_clickable)
                self.show()
        except AttributeError:
            pass

    def closeEvent(self, event: QCloseEvent) -> None:
        self.keyboard_listener.stop()
        event.accept()

    def update_label(self):
        name, artists = handle_spotify.get_current_track()
        self.lbl_songinfo.setText(f"{name} - {', '.join(artists)}")

    def toggle(self):
        if (is_playing := handle_spotify.is_currently_playing()) or is_playing is None:
            self.btn_pause.setIcon(QIcon("icons/play.png"))
            handle_spotify.pause()
        else:
            self.btn_pause.setIcon(QIcon("icons/pause.png"))
            handle_spotify.resume()

    @staticmethod
    def back():
        handle_spotify.back()

    @staticmethod
    def forward():
        handle_spotify.forward()

    # mouse press, move and releas event to make window draggable
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.offset = event.pos()
    #     else:
    #         super().mousePressEvent(event)
    #
    # def mouseMoveEvent(self, event):
    #     if self.offset is not None and event.buttons() == Qt.LeftButton:
    #         self.move(self.pos() + event.pos() - self.offset)
    #     else:
    #         super().mouseMoveEvent(event)
    #
    # def mouseReleaseEvent(self, event):
    #     self.offset = None
    #     super().mouseReleaseEvent(event)


app = QApplication([])
window = MainWindow()
window.show()
exit(app.exec())
