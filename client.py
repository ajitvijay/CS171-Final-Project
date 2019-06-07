import random
from socket import *
import threading
import _thread
import time
import config
import ast
import hashlib


def connectToNetwork(proc_num):
	NWSock = socket(AF_INET, SOCK_STREAM)

	while True:
		try:
			NWSock.connect(('127.0.0.1', config.serverPortNumber))
			break
		except:
			pass
	NWSock.send(bytes(str(proc_num), encoding='utf8'))
	return NWSock

def turnLetterIntoNum(letter):
	if letter.upper() == 'A':
		return 0
	else:
		if letter.upper() == 'B':
			return 1
		else:
			if letter.upper() == 'C':
				return 2
			else:
				if letter.upper() == 'D':
					return 3
				else:
					if letter.upper() == 'E':
						return 4

def sendTransaction(transaction, NWSock):
	newMessage = {}
	newMessage['type'] = 'transaction'
	newMessage['sender'] = -1
	newMessage['destination'] = turnLetterIntoNum(transaction[0])
	newMessage['transaction'] = transaction
	NWSock.send(bytes(str(newMessage) + '%' , encoding='utf8'))


def listen(connection):
	try:
		while True:
			msg = connection.recv(1024).decode()
			print(msg)
	finally:
		connection.close()

# alice = get_connection(config.server_ipaddress, config.alice_port)
# bob = get_connection(config.server_ipaddress, config.bob_port)
# carol = get_connection(config.server_ipaddress, config.carol_port)
# devon = get_connection(config.server_ipaddress, config.devon_port)
# elizabeth = get_connection(config.server_ipaddress, config.elizabeth_port)
NWSock = connectToNetwork(-1)
#_thread.start_new_thread(listen, (client, ))

# _thread.start_new_thread(listen, (alice, ))
# _thread.start_new_thread(listen, (bob, ))
# _thread.start_new_thread(listen, (carol, ))
# _thread.start_new_thread(listen, (devon, ))
# _thread.start_new_thread(listen, (elizabeth, ))

while(1):
	transaction = input("Enter Transaction: ")
	try:
		(sender, receiver, value) = transaction.split()
		transaction = (sender, receiver, value)
	except ValueError:
		print("invalid input format. must be Sender Receiver Money")
	if sender and receiver and value:
		sendTransaction(transaction,NWSock)
		print("client sent transaction")
