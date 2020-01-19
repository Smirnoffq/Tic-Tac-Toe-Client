from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from login_widget import LoginWidget
from lobby_widget import LobbyWidget
from game_widget import GameWidget

import sys
import socket

from messenger import Messenger
from listener import Listener
from sender import Sender


class MainWindow(QMainWindow):
    def __init__(self, parent=None, _sender=None):
        super().__init__(parent)
        port = 9999
        self.players = []
        self.games = []
        self.game_players = []

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', port))
        print("[+] Connected ")

        self.listener = Listener(self, self.client_socket)
        self.listener.start()
        self.sender = Sender(self.client_socket)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.setFixedWidth(1280)
        self.setFixedHeight(720)

        self.login_widget = self.prepareLoginWidget()
        self.central_widget.addWidget(self.login_widget)

        self.lobby_widget = self.prepareLobbyWidget()
        self.central_widget.addWidget(self.lobby_widget)

        self.game_widget = self.prepareGameWidget()
        self.central_widget.addWidget(self.game_widget)

        self.show()

    def closeEvent(self, event):  # nie działa, trzeba cos pokombinowac
        self.client_socket.shutdown(socket.SHUT_WR)
        self.listener.join()
        super(QMainWindow, self).closeEvent(event)

    def prepareLoginWidget(self):
        login_widget = LoginWidget(self)
        login_widget.pushButton.clicked.connect(self.login)

        return login_widget

    def prepareLobbyWidget(self):
        lobby_widget = LobbyWidget(self)
        lobby_widget.createGameButton.clicked.connect(self.createGame)
        lobby_widget.joinGameButton.clicked.connect(self.joinGame)

        return lobby_widget

    def prepareGameWidget(self):
        game_widget = GameWidget(self)
        game_widget.buttons[0][0].clicked.connect(lambda: self.makeMove(0, 0))
        game_widget.buttons[0][1].clicked.connect(lambda: self.makeMove(0, 1))
        game_widget.buttons[0][2].clicked.connect(lambda: self.makeMove(0, 2))
        game_widget.buttons[1][0].clicked.connect(lambda: self.makeMove(1, 0))
        game_widget.buttons[1][1].clicked.connect(lambda: self.makeMove(1, 1))
        game_widget.buttons[1][2].clicked.connect(lambda: self.makeMove(1, 2))
        game_widget.buttons[2][0].clicked.connect(lambda: self.makeMove(2, 0))
        game_widget.buttons[2][1].clicked.connect(lambda: self.makeMove(2, 1))
        game_widget.buttons[2][2].clicked.connect(lambda: self.makeMove(2, 2))

        return game_widget

    def login(self):
        nick = self.login_widget.lineEdit.text()

        if nick == "":
            return ""

        response = self.sender.send_login_request(nick)

    def updatePlayers(self, players):
        self.players = players

        print("Players: ", self.players)
        self.lobby_widget.playersTable.setRowCount(0)
        counter = 0

        for player in self.players:
            self.lobby_widget.playersTable.insertRow(counter)
            self.lobby_widget.playersTable.setItem(
                counter, 0, QTableWidgetItem(player["name"]))
            self.lobby_widget.playersTable.setItem(
                counter, 1, QTableWidgetItem(player["status"]))
            self.lobby_widget.playersTable.setItem(
                counter, 2, QTableWidgetItem(str(player["mmr"])))
            counter += 1

    def updateGames(self, games):
        self.games = games
        print("Games: ", self.games)

        self.lobby_widget.gamesTable.setRowCount(0)
        counter = 0

        for game in self.games:
            players = str(game["players_count"]) + "/2"

            self.lobby_widget.gamesTable.insertRow(counter)
            self.lobby_widget.gamesTable.setItem(
                counter, 0, QTableWidgetItem(game["name"]))
            self.lobby_widget.gamesTable.setItem(
                counter, 1, QTableWidgetItem(players))
            counter += 1

    def createGame(self):
        name = self.lobby_widget.gameNameEditLine.text()

        if name == "":
            return ""

        self.sender.send_create_game_request(name)
        self.lobby_widget.createGameButton.setEnabled(False)
        self.lobby_widget.joinGameButton.setEnabled(False)

    def joinGame(self):
        try:
            row = self.lobby_widget.gamesTable.selectedIndexes()[0]
        except IndexError as ie:
            self.lobby_widget.errorLabel.setText(
                "Wybierz gre do ktorej chcesz dolaczyc")
            return

        self.sender.send_join_game_request(int(self.games[row.row()]["id"]))
        self.lobby_widget.createGameButton.setEnabled(False)
        self.lobby_widget.joinGameButton.setEnabled(False)

    def makeMove(self, posX, posY):
        self.sender.send_make_move_request(posX, posY)

    def updateBoard(self, board):
        i = 0
        for row in board:
            j = 0
            for col in row:
                if col == self.game_players[0]["id"]:
                    self.game_widget.buttons[i][j].setIcon(
                        QIcon('tic-tac-toe-O.png'))
                elif col == self.game_players[1]["id"]:
                    self.game_widget.buttons[i][j].setIcon(
                        QIcon('tic-tac-toe-X.png'))
                else:
                    self.game_widget.buttons[i][j].setIcon(QIcon(''))
                j += 1
            i += 1

    def clearBoard(self):
        i = 0
        for row in range(3):
            j = 0
            for col in range(3):
                self.game_widget.buttons[i][j].setIcon(QIcon(''))
                j += 1
            i += 1
