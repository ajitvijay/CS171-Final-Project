import random
import time
import string
import threading
import _thread
from socket import *
import config
import ast
import sys
import hashlib
def balGreaterThanOrEqual(bal,ballotNum):
	if bal[0] > ballotNum[0]:
		return True
	else:
		if bal[0] == ballotNum[0] and bal[1] > ballotNum[1]:
			return True
		else:
			if bal[0] == ballotNum[0] and bal[1]== ballotNum[1]:
				return bal[2] >= ballotNum[2]

def sendPropAck(message,currentState,NWSock):
	newMessage = {}
	newMessage['type'] = 'prop_ack'
	newMessage['bal'] = message['bal']
	newMessage['acceptBal'] = currentState['acceptBal']
	newMessage['acceptVal'] = currentState['acceptVal']
	newMessage['destination'] = message['sender']
	newMessage['sender'] = message['destination']
	NWSock.send(bytes(str(newMessage), encoding='utf8'))
	return 0


def sendAccAck(message,NWSock):
	newMessage = {}
	newMessage['type'] = 'acc_ack'
	newMessage['bal'] = message['bal']
	newMessage['value'] = message['value']
	newMessage['destination'] = message['sender']
	newMessage['sender'] = message['destination']
	NWSock.send(bytes(str(newMessage), encoding='utf8'))
	return 0

def sendPropMessages(currentState,NWSock,newBlock):
	newMessage = {}
	newMessage['type'] = 'prop'
	newMessage['bal'] = (newBlock['depth'],currentState['BallotNum'][1]+1,currentState['proc_num'])
	newMessage['sender'] = currentState['proc_num']
	currentState['messagesReceived'] = []
	currentState['state'] = 'waiting for prop_ack'
	for server in [0,1,2,3,4]:
		newMessage['destination'] = server
		if newMessage['destination'] == newMessage['sender']:
			receiveMessage(newMessage,currentState,NWSock,transactions)
		else:
			NWSock.send(bytes(str(newMessage) , encoding='utf8'))
	return 0



	def sendDecisionMessages(currentState,NWSock,transactions):
	newMessage = {}
	newMessage['type'] = 'decision'
	newMessage['bal'] = currentState['messagesReceived'][0]['bal']
	newMessage['value'] = currentState['messagesReceived'][0]['value']
	newMessage['sender'] = currentState['messagesReceived'][0]['destination']
	currentState['messagesReceived'] = []
	for server in [0,1,2,3,4]:
		newMessage['destination'] = server
		if newMessage['destination'] == newMessage['sender']:
			receiveMessage(newMessage,currentState,NWSock,transactions)
		else:
			NWSock.send(bytes(str(newMessage) , encoding='utf8'))
	return 0

def sendAccMessages(currentState,NWSock,transactions):
	value = None
	b = None
	for message in currentState['messagesReceived']:
		if message['value'] != 'N/A':
			if balGreaterThanOrEqual(message['acceptBal'],b)
				value = message['acceptVal']
				b= message['acceptBal']
	newMessage = {}
	newMessage ['type'] = 'acc'
	newMessage ['bal'] = currentState['messagesReceived'][0]['bal']
	if value is not None:		
		newMessage['value'] = value
	else:
		newMessage['value'] = currentState['value'] 
	newMessage['sender'] = currentState['messagesReceived'][0]['destination']

	currentState['messagesReceived'] = []
	currentState['state'] = 'waiting for acc_ack'

	for server in [0,1,2,3,4]:
		newMessage['destination'] = server
		if newMessage['destination'] == newMessage['sender']:
			receiveMessage(newMessage,currentState,NWSock,transactions)
	    else:
	    	NWSock.send(bytes(str(newMessage) , encoding='utf8'))

def receiveMessage(message,currentState,NWSock,transactions):
	if message['type'] =='prop_ack' and currentState['state'] == 'waiting for prop_ack':
		currentState['messagesReceived'].append(message)
		if len(currentState['messagesReceived']) >= 3:
			sendAccMessages(currentState['messagesReceived'],currentState,NWSock,transactions)
	else:
		if message['type'] == 'acc_ack' and currentState['state'] == 'waiting for acc_ack':
			currentState['messagesReceived'].append(message)
			if len(currentState['messagesReceived']) >= 3:
				sendDecisionMessages(currentState['messagesReceived'],currentState,NWSock,transactions)
		else:
			if message['type'] == 'prop':
				if balGreaterThanOrEqual(message['bal'],currentState['BallotNum']):
					currentState['BallotNum'] = message['bal']
					sendPropAck(message,currentState,NWSock)
			else:
				if message['type'] == 'acc':
					if balGreaterThanOrEqual(message['bal'],currentState['BallotNum']):
						currentState['acceptBal']=message['bal']
						currentState['acceptVal'] = message['value']
						sendAccAck(message,NWSock)
				else:
					if message['type'] == 'decision':
						#if decided value is from this proc_num
						if currentState['proc_num'] == currentState['messagesReceived'][0]['bal'][2]:
							transactions.remove(transactions[0])
							transactions.remove(transactions[1])


						currentState['state'] = 'N/A'
						currentState['value'] = 'N/A'
						currentState['acceptBal'] = 'N/A'
						currentState['acceptVal'] = 'N/A'
						currentState['mostRecentResponse'] = 'N/A'

						currentState['messagesReceived'] = []
						currentState['blockChain'].append(message['value'])


						currentState['BallotNum'] = (len(blockChain), currentState['BallotNum'][1],currentState['proc_num'])
					else: 
						if message['type'] == 'sync':
							newMessage = {}
							newMessage['type'] = 'sync-response'
							newMessage['data'] = currentState['blockChain']
							NWSock.send(bytes(str(newMessage) , encoding='utf8'))

	return 0


# def run(proc_num,NWconfigFile):
# 	blockChain = []

# 	currentState['messagesReceived'] = []
	

# 	networkPort = readConfigFile(NWconfigFile)
# 	try:
# 	    nwSock.connect(('127.0.0.1', networkPort))

# 	while True:
#         time.sleep(1)

#         try:
#             client, addr = clientSock.accept()
#             print('Got connection with client at ', addr)
#             client.setblocking(0)

#         except socket.error as err:
#             pass

#         # manage sending a message when received one from client
#         try:
#             if client is not None:
#                 messageString = client.recv(1024).decode('utf-8')

#                 if messageString != '':
#                     print("Received transaction request from client ")
#                     messageDict = ast.literal_eval(str(messageString))
#                     #include trans code here

#         except socket.error as err:
#             pass

#         # Manage receiving a message from the network
#         try:
#             if nwSock is not None:
#                 messageString = nwSock.recv(1024).decode('utf-8')

#                 if messageString != '':
#                     messageStrings = separateMessages(messageString)

#                     for message in messageStrings:
#                         messageDict = ast.literal_eval(str(message))
#                         receiveMessage(messageDict, currentState,currentState['messagesReceived'], nwSock)

#         except socket.error as err:
#             pass
# 	return 0

def transaction_message(networkSocket, client_conn,proc_num):
	currentState = {}
	currentState['state']= 'N/A'
	currentState['acceptVal']= 'N/A'
	currentState['acceptBal']= 'N/A'
	#is default value for when a block is successfully mined:
	currentState['value']= 'N/A'
	currentState['BallotNum']= (0,0,proc_num)
	currentState['proc_num']= proc_num
	currentState['mostRecentResponse'] = 'N/A'

	currentState['messagesReceived'] = []
	networkSocket.setblocking(0)

	try:
		while True:
			global clientName
			global serverName
			global transactions
			global blockChain
			transact_msg = client_conn.recv(1024).decode()
			(sender, receiver, amt) = transact_msg.split()
			transactions.append(transact_msg)
			print((sender,receiver,amt))
			print(transactions)
			# msg = transactions[0] + get_random_string()
			# value = hashlib.sha256(msg.encode()).hexdigest()
			# print(value)
			# print(type(value))
			# print(value[-1])
			# print(type(value[-1])) #type string

			if(len(transactions) > 1):
				(nonce_hash_value, transact_list, nonce_string) = get_hash(transactions)
				print(nonce_hash_value)
				print(transact_list)
				print(nonce_string)
				if len(blockChain) == 0: #check to see if blockChain has any previous validated blocks
					prevhash = "NULL"
				else:
					(prev_nonce_hash, prev_transact_list, prev_nonce_string) = blockChain[len(blockChain)-1]
					hasher_str = prev_nonce_hash + prev_transact_list[0] + prev_transact_list[1] + prev_nonce_string + str(len(blockChain)-1)
					prevhash = hashlib.sha256(hasher_str.encode()).hexdigest()
					
				# IF BLOCK IS VALID RUN THIS FUNCTION:
				# sendPropMessages(currentState,networkSocket,newBlock,transactions)

			# receive message and then process if received
			try:
				receivedMessage = networkSocket.recv(1024).decode()
                messageDict = ast.literal_eval(messageString)
                receiveMessage(messageDict,currentState,currentState['messagesReceived'],networkSocket,transactions):


			except socket.error as err:

			if currentState['mostRecentResponse'] != "N/A":
				currentTime = datetime.datetime.now()
				#get time passed since this response
				if time_passed > threshold:




	finally:
		client_conn.close()

def get_random_string():
	random_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]) #length of 10
	return random_str


def get_hash(transactions):
	trans_list = []
	trans_list.append(transactions[0])
	trans_list.append(transactions[1])
	temp = True
	while(temp):
		rdstr = get_random_string()
		msg = transactions[0] + transactions[1] + rdstr
		value = hashlib.sha256(msg.encode()).hexdigest()
		checker = value[-1]
		# print(value)
		# print(checker)
		if checker.isdigit() == True:
			if int(checker) == 0 or int(checker) == 1:
				return value, trans_list, rdstr
			else:
				continue


####### MAIN STARTS HERE
####### ALL HELPER FUNCTIONS GO BEFORE
serverSocket = socket(AF_INET, SOCK_STREAM)
networkSocket = socket(AF_INET, SOCK_STREAM)
transactions = []
blockChain = []

if(len(sys.argv) < 2):
	print("must indicate what server this is")
	exit()

serverName = sys.argv[1]
if serverName == 'A':
	serverSocket.bind((config.server_ipaddress, config.alice_port))
	clientName = 'a'
if serverName == 'B':
	serverSocket.bind((config.server_ipaddress, config.bob_port))
	clientName = 'b'
if serverName == 'C':
	serverSocket.bind((config.server_ipaddress, config.carol_port))
	clientName = 'c'
if serverName == 'D':
	serverSocket.bind((config.server_ipaddress, config.devon_port))
	clientName = 'd'
if serverName == 'E':
	serverSocket.bind((config.server_ipaddress, config.elizabeth_port))
	clientName = 'e'

serverSocket.listen(5)
(nw_conn, nw_addr) = serverSocket.accept()
print("Connection %s from nw server received", nw_conn)
networkSocket.connect((config.server_ipaddress, config.network_port))
(client_conn, client_addr) = serverSocket.accept()
_thread.start_new_thread(transaction_message, (networkSocket,client_conn))
while True:
	continue
