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

alice = get_connection(config.server_ipaddress, alice_port)
bob = get_connection(config.server_ipaddress, bob_port)
carol = get_connection(config.server_ipaddress, carol_port)
devon = get_connection(config.server_ipaddress, devon_port)
elizabeth = get_connection(config.server_ipaddress, elizabeth_port)

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
		# you left off here
		# determine who is the sender and then send message to network process
