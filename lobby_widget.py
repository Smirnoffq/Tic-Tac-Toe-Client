from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LobbyWidget(QWidget):
    def __init__(self, parent=None):
        super(LobbyWidget, self).__init__(parent)
        layout = QHBoxLayout()
        self.label = QLabel('logged in!')
        layout.addWidget(self.label)
        self.setLayout(layout)

