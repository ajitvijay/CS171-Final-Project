import random
from socket import *
import time
import config
import threading
import ast

def message_parser(connection, address):
    global aliceSocket
    global bobSocket
    global carolSocket
    global devonSocket
    global elizabethSocket
    message_type = ""
    try:
        connectionfrom = address + " has connected to network process"
        print(connectionfrom)
        while True:
            message = connection.recv(1024)
            try:
                (sender, receiver, value) = message.split()
                message_type = "transaction"
                print(message)
            except ValueError:
                print("not a transaction message")
    finally:
        connection.close()

networkSocket = socket(AF_INET, SOCK_STREAM)
networkSocket.bind((config.server_ipaddress, config.network_port))
networkSocket.listen(5)

aliceSocket = socket(AF_INET, SOCK_STREAM)
bobSocket = socket(AF_INET, SOCK_STREAM)
carolSocket = socket(AF_INET, SOCK_STREAM)
devonSocket = socket(AF_INET, SOCK_STREAM)
elizabeth = socket(AF_INET, SOCK_STREAM)

aliceSocket.connect((config.server_ipaddress, config.alice_port))
bobSocket.connect((config.server_ipaddress, config.bob_port))
carolSocket.connect((config.server_ipaddress, config.carol_port))
devonSocket.connect((config.server_ipaddress, config.devon_port))
elizabethSocket.connect((config.server_ipaddress, config.elizabeth_port))

while True:
    conn, addr = networkSocket.accept()
    thread.start_new_thread(message_parser, (conn, addr))
