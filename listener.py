from PyQt5.QtCore import *

import socket
import threading
import traceback

from messenger import Messenger


class Listener (threading.Thread):
    def __init__(self, _mainWindow, _socket):
        threading.Thread.__init__(self)
        self.mainWindow = _mainWindow
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
                break  # user disconnected

            try:
                self.handle_message(message)
            except Exception as e:
                print(e)
                traceback.print_tb(e.__traceback__)

    def handle_message(self, message):
        response_handlers = [self.handle_login_response, self.handle_game_managment_response,
                             self.handle_game_move_response, self.handle_lists_response]
        info_handlers = [self.handle_win_condition,
                         self.handle_game_board, self.handle_lists]

        try:
            isResponse = message["isResponse"]
        except Exception as e:
            isResponse = False

        if isResponse:
            result = response_handlers[message["operation"]](message)
        else:
            result = info_handlers[int(message["operation"]) - 1](message)

    '''
    To jest tak bardzo 'hack' ze az mi szkoda slów ale działać działa
    Ogólnie to powinno sie sygnal do main_window wysłać ale teraz to za pozno
    '''
    def handle_login_response(self, message):
        if message["status"] == False:
            self.mainWindow.login_widget.label_2.setText(message["message"])
            return ""
        
        self.mainWindow.central_widget.setCurrentWidget(self.mainWindow.lobby_widget)

    def handle_game_managment_response(self, message):
        pass

    def handle_game_move_response(self, message):
        pass

    def handle_lists_response(self, message):
        pass

    def handle_win_condition(self, message):
        pass

    def handle_game_board(self, message):
        pass

    def handle_lists(self, message):
        pass