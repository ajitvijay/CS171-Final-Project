import random
from socket import *
import threading
import time
import config
import ast


def get_connection(ip_address, port_server):
	client_socket = socket(AF_INET, SOCK_STREAM)
	client_socket.connect((ip_address,port_server))
	return client_socket

def listen(connection):
	try:
		while True:
			msg = connection.recv(1024)
			print(msg)
	finally:
		connection.close()

alice = get_connection(config.server_ipaddress, config.alice_port)
bob = get_connection(config.server_ipaddress, config.bob_port)
carol = get_connection(config.server_ipaddress, config.carol_port)
devon = get_connection(config.server_ipaddress, config.devon_port)
elizabeth = get_connection(config.server_ipaddress, config.elizabeth_port)

thread.start_new_thread(listen, (alice, ))
thread.start_new_thread(listen, (bob, ))
thread.start_new_thread(listen, (carol, ))
thread.start_new_thread(listen, (devon, ))
thread.start_new_thread(listen, (elizabeth, ))

while true:
	transaction = input("Enter Transaction: ")

	try:
		(sender, receiver, value) = transaction.split()
	except ValueError:
		print("invalid input format. must be Sender Receiver Money")
	if sender and receiver and value:
		if sender == 'A':
			alice.send(transaction)
		if sender == 'B':
			bob.send(transaction)
		if sender == 'C':
			carol.send(transaction)
		if sender == 'D':
			devon.send(transaction)
		if sender == 'E':
			elizabeth.send(transaction)
