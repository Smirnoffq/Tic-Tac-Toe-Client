import socket
import threading

from messenger import Messenger

class Listener (threading.Thread):

    def __init__(self, _socket):
        threading.Thread.__init__(self)
        self.socket = _socket
        self.delete_self = False

    def run(self):
        while True:
            if self.delete_self:
                break

            try:
                message = Messenger.receive(self.socket)
                message = Messenger.decode_data(message)
                print("New message: ", message)
            except RuntimeError as re:
                print(re)
                self.delete_self = True
                break # user disconnected

            try:
                self.handle_message(message)
            except Exception as e:
                pass

    def handle_message(message):
        pass
