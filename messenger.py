import base64
import json

class Messenger:
    MSG_LEN = 4096

    @staticmethod
    def encode_data(data):
        if not isinstance(data, dict):
            raise Exception("Wrong input data")

        json_data = json.dumps(data).encode("utf-8")
        base64_data = base64.b64encode(json_data) + b';'
        
        return base64_data + (b'0' * (Messenger.MSG_LEN - len(base64_data)))

    @staticmethod
    def decode_data(data):
        if b';' not in data:
            raise Exception("Wrong input data: missing ';'")

        data = data.split(b';')[0]
        json_data = base64.b64decode(data)
        decoded_data = json.loads(json_data)
        
        return decoded_data

    @staticmethod
    def get_players_list_msg():
        msg = {}
        msg["operation"] = 3
        msg["sub_operation"] = 1

        return msg

    @staticmethod
    def get_games_list_msg():
        msg = {}
        msg["operation"] = 3
        msg["sub_operation"] = 0

        return msg

    @staticmethod
    def login_msg(nickname):
        msg = {}
        msg["operation"] = 0
        msg["sub_operation"] = 0
        msg["name"] = nickname

        return msg

    @staticmethod
    def logout_msg():
        msg = {}
        msg["operation"] = 0
        msg["sub_operation"] = 1

        return msg

    @staticmethod
    def create_game_msg(game_name):
        msg = {}
        msg["operation"] = 1
        msg["sub_operation"] = 0
        msg["name"] = game_name

        return msg

    @staticmethod
    def join_game_msg(game_id):
        msg = {}
        msg["operation"] = 1
        msg["sub_operation"] = 1
        msg["id"] = game_id

        return msg
    
    @staticmethod
    def leave_game_msg():
        msg = {}
        msg["operation"] = 1
        msg["sub_operation"] = 2

        return msg

    @staticmethod
    def make_move_msg(posX, posY):
        msg = {}
        msg["operation"] = 2
        msg["sub_operation"] = 0
        msg["posX"] = int(posX)
        msg["posY"] = int(posY)

        return msg

    @staticmethod
    def receive(socket):
        msg = b''
        while b';' not in msg and len(msg) < Messenger.MSG_LEN:
            
            chunk = socket.recv(min(Messenger.MSG_LEN - len(msg), Messenger.MSG_LEN))
            if chunk == b'':
                raise Exception("Socket disconnected")
            msg = msg + chunk
        return msg

    @staticmethod
    def send(data, socket):
        sent_count = 0
        while sent_count < Messenger.MSG_LEN:
            sent = socket.send(data[sent_count:])
            if sent == 0:
                raise Exception("Socket disconnected")
            sent_count = sent_count + sent