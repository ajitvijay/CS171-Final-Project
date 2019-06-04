import random
from socket import *
import time
import config
import threading
import _thread
import ast
import hashlib

def rand_delay():
    time_delay = random.uniform(1.0,4.0)
    time.sleep(time_delay)
    print("random delay is %s seconds", time_delay)
    return time_delay

def message_parser(connection, address):
    global aliceSocket
    global bobSocket
    global carolSocket
    global devonSocket
    global elizabethSocket
    message_type = ""
    try:
        connectionfrom = "NW has received connection from ", address
        print(connectionfrom)
        while True:
            message = connection.recv(1024).decode()
            try:
                (sender, receiver, value) = message.split()
                message_type = "transaction"
                print(message)
                if sender == 'A':
                    rand_delay()
                    aliceSocket.send(message.encode())
                if sender == 'B':
                    rand_delay()
                    bobSocket.send(message.encode())
                if sender == 'C':
                    rand_delay()
                    carolSocket.send(message.encode())
                if sender == 'D':
                    rand_delay()
                    devonSocket.send(message.encode())
                if sender == 'E':
                    rand_delay()
                    elizabethSocket.send(message.encode())
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
elizabethSocket = socket(AF_INET, SOCK_STREAM)

aliceSocket.connect((config.server_ipaddress, config.alice_port))
bobSocket.connect((config.server_ipaddress, config.bob_port))
carolSocket.connect((config.server_ipaddress, config.carol_port))
devonSocket.connect((config.server_ipaddress, config.devon_port))
elizabethSocket.connect((config.server_ipaddress, config.elizabeth_port))

while True:
    conn, addr = networkSocket.accept()
    _thread.start_new_thread(message_parser, (conn, addr))
