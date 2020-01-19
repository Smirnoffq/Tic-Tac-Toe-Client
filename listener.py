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
        info_handlers = [self.handle_game_info, self.handle_win_condition,
                         self.handle_game_board, self.handle_lists]

        try:
            isResponse = message["isResponse"]
        except Exception as e:
            isResponse = False

        if isResponse:
            result = response_handlers[message["operation"]](message)
        else:
            result = info_handlers[int(message["operation"])](message)

    '''
    To jest tak bardzo 'hack' ze az mi szkoda slów ale działać działa
    Ogólnie to powinno sie sygnal do main_window wysłać ale teraz to za pozno
    '''

    def handle_login_response(self, message):
        if message["status"] == False:
            self.mainWindow.login_widget.label_2.setText(message["message"])
            return ""

        self.mainWindow.central_widget.setCurrentWidget(
            self.mainWindow.lobby_widget)
        self.mainWindow.sender.send_get_games_request()
        self.mainWindow.sender.send_get_players_request()

    def handle_game_managment_response(self, message):
        self.mainWindow.lobby_widget.createGameButton.setEnabled(True)
        self.mainWindow.lobby_widget.joinGameButton.setEnabled(True)

        if message["status"] == False:
            self.mainWindow.lobby_widget.errorLabel.setText(message["message"])
            return

        if int(message["sub_operation"]) == 0:  # create game
            self.mainWindow.central_widget.setCurrentWidget(
                self.mainWindow.game_widget)
            self.mainWindow.game_widget.statusLabel.setText("Your move!")
        else:
            self.mainWindow.central_widget.setCurrentWidget(
                self.mainWindow.game_widget)
            self.mainWindow.game_widget.statusLabel.setText("Your opponent's move")

    def handle_game_move_response(self, message):
        if message["status"] == False:
            self.mainWindow.game_widget.statusLabel.setText(message["message"])
            return

        self.mainWindow.game_widget.statusLabel.setText("Your move!")

    def handle_lists_response(self, message):
        self.handle_lists(message)

    def handle_win_condition(self, message):
        winner = message["message"]["winner"]
        loser = message["message"]["loser"]

        self.mainWindow.lobby_widget.errorLabel.setText(message["message"]["message"])
        self.mainWindow.sender.send_get_players_request()
        self.mainWindow.sender.send_get_games_request()
        self.mainWindow.clearBoard()
        self.mainWindow.central_widget.setCurrentWidget(
            self.mainWindow.lobby_widget)

    def handle_game_board(self, message):
        self.mainWindow.updateBoard(message["message"])
    
    def handle_game_info(self, message):
        if message["sub_operation"] == int(0):
            self.mainWindow.game_players = message["message"]
            if message["message"][0] != None:
                msg = "Player O: " + message["message"][0]["name"] + " (" + str(message["message"][0]["mmr"]) +" MMR)"
                self.mainWindow.game_widget.player0Label.setText(msg)

            if message["message"][1] != None:
                msg = "Player X: " + message["message"][1]["name"] + " (" + str(message["message"][1]["mmr"]) +" MMR)"
                self.mainWindow.game_widget.player1Label.setText(msg)

    def handle_lists(self, message):
        if message["sub_operation"] == int(0):  # games list
            self.mainWindow.updateGames(message["message"])
        elif message["sub_operation"] == int(1):  # players list
            self.mainWindow.updatePlayers(message["message"])
