from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from login_widget import LoginWidget
from lobby_widget import LobbyWidget

import sys
import socket

from messenger import Messenger
from listener import Listener
from sender import Sender

class MainWindow(QMainWindow):
    def __init__(self, parent=None, _sender=None):
        super().__init__(parent)
        port = 9999
    
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', port))
        print("[+] Connected ")

        self.listener = Listener(self.client_socket)
        self.listener.start()
        self.sender = Sender(self.client_socket)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setFixedWidth(1280)
        self.setFixedHeight(720)

        self.login_widget = self.prepareLoginWidget()
        self.central_widget.addWidget(self.login_widget)

        self.show()

    def closeEvent(self, event): # nie działa, trzeba cos pokombinowac
        self.client_socket.shutdown(socket.SHUT_WR)
        self.listener.join()
        super(QMainWindow, self).closeEvent(event)

    def prepareLoginWidget(self):
        login_widget = LoginWidget(self)
        login_widget.pushButton.clicked.connect(self.login)

        return login_widget

    def login(self):
        nick = self.login_widget.lineEdit.text()

        if nick == "":
            return ""

        response = self.sender.send_login_request(nick)

        if response["status"] == False:
            self.login_widget.label_2.setText(response["message"])
            return ""
        
        logged_in_widget = LobbyWidget(self)
        self.central_widget.addWidget(logged_in_widget)
        self.central_widget.setCurrentWidget(logged_in_widget)
