import random
import socket
import threading
import time
import ast


def get_connection(ip_address, port_server):
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect((ip_address,port_server))
	return client_socket

def listen(connection):
	try:
		while True:
			msg = connection.recv(1024)
			print msg
	finally:
		connection.close()
