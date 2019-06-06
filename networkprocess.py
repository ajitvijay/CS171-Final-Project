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
    print("random delay is %f seconds!", time_delay)
    return time_delay

def message_parser(connection, address, connection_list):
    global aliceSocket
    global bobSocket
    global carolSocket
    global devonSocket
    global elizabethSocket
    global clientSocket
    message_type = ""
    alice_conn = connection_list[0]
    bob_conn = connection_list[1]
    carol_conn = connection_list[2]
    devon_conn = connection_list[3]
    elizabeth_conn = connection_list[4]
    client_conn = connection_list[5]
    if connection == address:
        return 0
    else:
        try:
            connectionfrom = "NW has received connection from ", address
            while True:
                try:
                    message = connection.recv(1024).decode()
                    print(message)
                    (sender, receiver, value) = message.split()
                    message_type = "transaction"
                    print(connection_list)
                    if sender == 'A':
                        if alice_conn != 0:
                            rand_delay()
                            alice_conn.send(message.encode())
                            print("message has been sent to server")
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
                except:
                    pass

        finally:
            connection.close()

def connection_attempt(sock):
    sock.setblocking(0)
    try:
        conn, addr = sock.accept()
        return conn, addr
    except:
        return 0, 0


networkSocket = socket(AF_INET, SOCK_STREAM)
networkSocket.bind((config.server_ipaddress, config.network_port))
networkSocket.listen(6)

aliceSocket = socket(AF_INET, SOCK_STREAM)
bobSocket = socket(AF_INET, SOCK_STREAM)
carolSocket = socket(AF_INET, SOCK_STREAM)
devonSocket = socket(AF_INET, SOCK_STREAM)
elizabethSocket = socket(AF_INET, SOCK_STREAM)
clientSocket = socket(AF_INET, SOCK_STREAM)

aliceSocket.bind((config.server_ipaddress, config.alice_port))
bobSocket.bind((config.server_ipaddress, config.bob_port))
carolSocket.bind((config.server_ipaddress, config.carol_port))
devonSocket.bind((config.server_ipaddress, config.devon_port))
elizabethSocket.bind((config.server_ipaddress, config.elizabeth_port))
clientSocket.bind((config.server_ipaddress, config.client_port))

aliceSocket.listen(6)
bobSocket.listen(6)
carolSocket.listen(6)
devonSocket.listen(6)
elizabethSocket.listen(6)
clientSocket.listen(6)

while True:
    # alice_conn, alice_addr = aliceSocket.accept()
    # bob_conn, bob_addr = bobSocket.accept()
    # carol_conn, carol_addr = carolSocket.accept()
    # devon_conn, devon_addr = devonSocket.accept()
    # elizabeth_conn, elizabeth_addr = elizabethSocket.accept()
    # client_conn, client_addr = clientSocket.accept()
    alice_conn, alice_addr = connection_attempt(aliceSocket)
    bob_conn, bob_addr = connection_attempt(bobSocket)
    carol_conn, carol_addr = connection_attempt(carolSocket)
    devon_conn, devon_addr = connection_attempt(devonSocket)
    elizabeth_conn, elizabeth_addr = connection_attempt(elizabethSocket)
    client_conn, client_addr = connection_attempt(clientSocket)
    # list of client connections isnt getting the right values because it doesn't get initialized until after servers all connect
    connections = []
    connections.append(alice_conn)
    connections.append(bob_conn)
    connections.append(carol_conn)
    connections.append(devon_conn)
    connections.append(elizabeth_conn)
    connections.append(client_conn)
    print(connections)
    _thread.start_new_thread(message_parser, (alice_conn, alice_addr, connections))
    _thread.start_new_thread(message_parser, (bob_conn, bob_addr, connections))
    _thread.start_new_thread(message_parser, (carol_conn, carol_addr, connections))
    _thread.start_new_thread(message_parser, (devon_conn, devon_addr, connections))
    _thread.start_new_thread(message_parser, (elizabeth_conn, elizabeth_addr, connections))
    _thread.start_new_thread(message_parser, (client_conn, client_addr, connections))
