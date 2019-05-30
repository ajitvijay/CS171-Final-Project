import random
import time
import threading
import ast

def get_connection(ip_address, port_server):
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect((ip_address,port_server))
	return client_socket

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
            except: ValueError
                print "not a transaction message"
    finally:
        connection.close()

networkSocket = socket(AF_INET, SOCK_STREAM)
networkSocket.bind((config.server_ipaddress, config.network_port))
networkSocket.listen(5)

alice = get_connection(config.server_ipaddress, alice_port)
bob = get_connection(config.server_ipaddress, bob_port)
carol = get_connection(config.server_ipaddress, carol_port)
devon = get_connection(config.server_ipaddress, devon_port)
elizabeth = get_connection(config.server_ipaddress, elizabeth_port)

while True:
    conn, addr = networkSocket.accept()
    thread.start_new_thread(message_parser, (conn, addr))
