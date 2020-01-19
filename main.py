import sys
import socket
import time

from messenger import Messenger
from listener import Listener
from sender import Sender

from main_window import MainWindow
from PyQt5.QtWidgets import *


def main(args):
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = MainWindow()
    # client_socket.shutdown(socket.SHUT_WR)
    # listener.join()

    sys.exit(app.exec())


if __name__ == "__main__":

    main(sys.argv)
