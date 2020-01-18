import socket
import threading

from messenger import Messenger

class Sender ():

    def __init__(self, _socket):
        self.socket = _socket

    def sending_loop(self):
        while True:
            print("[0] Login\n[1] Logout\n[2] Create game\n[3] Join game\n[4] Make move\n[5] Get games list\n[6] Get players list\n[7] Leave game ")
            decision = int(input("Co chcesz zrobic? "))

            if decision == 0:
                name = input("Podaj nick ")
                msg = self.send_and_receive_msg(Messenger.login_msg(name))
                print("Response: ", msg)
            elif decision == 1:
                msg = self.send_and_receive_msg(Messenger.logout_msg())
                print("Response: ", msg)
                break
            elif decision == 2:
                name = input("Podaj nazwe ")
                msg = self.send_and_receive_msg(Messenger.create_game_msg(name))
                print(msg)
            elif decision == 3:
                g_id = int(input("Podaj id "))
                msg = self.send_and_receive_msg(Messenger.join_game_msg(g_id))
                print(msg)
            elif decision == 4:
                posX = int(input("Podaj X "))
                posY = int(input("Podaj Y "))
                msg = self.send_and_receive_msg(Messenger.make_move_msg(posX, posY))
                print(msg)
            elif decision == 5:
                msg = self.send_and_receive_msg(Messenger.get_games_list_msg())
                print(msg)
            elif decision == 6:
                msg = self.send_and_receive_msg(Messenger.get_players_list_msg())
                print(msg)
            elif decision == 7:
                msg = self.send_and_receive_msg(Messenger.leave_game_msg())
                print(msg)

    def send_and_receive_msg(self, message):
        msg = Messenger.encode_data(message)
        Messenger.send(msg, self.socket)
        msg = Messenger.receive(self.socket)
        msg_d = Messenger.decode_data(msg)

        return msg_d

    def send_msg(self, message):
        msg = Messenger.encode_data(message)
        Messenger.send(msg, self.socket)

    def send_logout_request(self):
        self.send_msg(Messenger.logout_msg())

    def send_login_request(self, nickname):
        self.send_msg(Messenger.login_msg(nickname))

    def send_create_game_request(self, name):
        self.send_msg(Messenger.create_game_msg(name))

    def send_join_game_request(self, id):
        self.send_msg(Messenger.join_game_msg(g_id))

    def send_make_move_request(self, posX, posY):
        self.send_msg(Messenger.make_move_msg(posX, posY))

    def send_get_games_request(self, nickname):
        self.send_msg(Messenger.get_games_list_msg())

    def send_get_players_request(self, nickname):
        self.send_msg(Messenger.get_players_list_msg(name))

    def send_leave_game_request(self, nickname):
        self.send_msg(Messenger.leave_game_msg())