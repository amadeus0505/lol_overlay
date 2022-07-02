from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore, QtGui


class IconButton(QPushButton):
    def __init__(self):
        super(IconButton, self).__init__()
        self.icon_size = 30
        self.icon_grow = 4
        self.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))
        self.setFont(QtGui.QFont("Times", 15))
        self.setFixedWidth(35)

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.setIconSize(QtCore.QSize(self.icon_size + self.icon_grow, self.icon_size + self.icon_grow))
        super().enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setIconSize(QtCore.QSize(self.icon_size, self.icon_size))

