import sys
import socket
import time

from messenger import Messenger
from sender import Sender
from listener import Listener

def main(args):
    port = 9999
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', port))
    print("[+] Connected ")

    listener = Listener(client_socket)
    listener.start()
    sender = Sender(client_socket)
    sender.sending_loop()

    client_socket.shutdown(socket.SHUT_WR)
    listener.join()

if __name__ == "__main__":
    main(sys.argv)