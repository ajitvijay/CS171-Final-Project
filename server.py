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

initialBalances = {'A': 100, 'B': 100, 'C': 100, 'D': 100, 'E': 100}
timeOutDuration = 15


def balGreaterThanOrEqual(bal,BallotNum):
	if bal[0] > BallotNum[0]:
		return True
	else:
		if bal[0] == BallotNum[0] and bal[1] > BallotNum[1]:
			return True
		else:
			if bal[0] == BallotNum[0] and bal[1]== BallotNum[1]:
				return bal[2] >= BallotNum[2]

def saveData(currentState):
	pass

def readData(currentState):
	pass

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
	newMessage['bal'] = (getDepthNumFromBlock(newBlock),currentState['BallotNum'][1]+1,currentState['proc_num'])
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

def sendSync(currentState,NWSock):
	#synchronize if new block is not the next block
		newMessage = {}
		newMessage['type'] = 'sync'
		newMessage['blockChainLength'] = len(currentState['blockChain'])
		newMessage['bal'] = currentState['BallotNum']
		newMessage['sender'] = currentState['proc_num']
		NWSock.send(bytes(str(newMessage) , encoding='utf8'))

		for server in [0,1,2,3,4]:
			newMessage['destination'] = server
			if newMessage['destination'] == newMessage['sender']:
				pass
		    else:
		    	NWSock.send(bytes(str(newMessage) , encoding='utf8'))



def sendSyncResponse(currentState,message,NWSock):
	newMessage = {}
	newMessage['type'] = 'sync-response'
	newMessage['data'] = currentState['blockChain'][message['blockChainLength']:]
	newMessage['bal'] = currentState['BallotNum']
	newMessage['sender'] = message['destination']
	newMessage['destination'] = message['sender'] 
	
	NWSock.send(bytes(str(newMessage) , encoding='utf8'))



def sendTransSet(currentState,NWSock):
	newMessage = {}
	newMessage['type'] = 'trans-set'
	newMessage['sender'] = currentState['proc_num']
	newMessage['destination'] = '-1'
	newMessage['transactions'] = currentState['transactions']
	NWSock.send(bytes(str(newMessage) , encoding='utf8'))

def sendBalance(currentState,NWSock):

	newMessage = {}
	newMessage['type'] = 'balances'
	newMessage['sender'] = currentState['proc_num']
	newMessage['destination'] = -1
	newMessage['balances'] = calculateBalance(currentState)
	newMessage['depth'] = len(currentState['blockChain'])

	NWSock.send(bytes(str(newMessage) , encoding='utf8'))


def sendBlockChain(currentState,NWSock):
	newMessage = {}
	newMessage['type'] = 'balances'
	newMessage['sender'] = currentState['proc_num']
	newMessage['destination'] = -1
	newMessage['blockChain'] = currentState['blockChain']
	NWSock.send(bytes(str(newMessage) , encoding='utf8'))

def rejectTrans(transaction,NWSock):
	newMessage = {}
	newMessage['type'] = 'failure'
	newMessage['sender'] = currentState['proc_num']
	newMessage['destination'] = -1
	newMessage['msg'] = 'Transaction Failed'
	newMessage['data'] = transaction

def receiveDecision(currentState,message,NWSock):
# NEED ADD THING BELOW:
	if len(currentState['blockChain']) + 1 != getDepthNumFromBlock(message['value']):
		#check to see if we have second decision:
		if len(currentState['blockChain']) == getDepthNumFromBlock(message['value']):
			pass
		else:
			print('Received decision out of order, updating blockchain now for all blocks past:' + str(newMessage['blockChainLength']))
			time.sleep(7)
			sendSync(currentState,NWSock)							
	else:
		# The block is the next in the chain. Now we validate the transactions
		validityCheck = checkIfTransactionsAreValid(currentState,NWSock,transactions)
		if validityCheck == [True,True]:
		
			#if decided value is from this proc_num
			if currentState['proc_num'] == message['sender']:
				trans = currentState['transactions'][:2]
				currentState['transactions'].remove(trans[0])
				currentState['transactions'].remove(trans[1])

			# because we added a new block, we have to reset paxos states
			currentState['state'] = 'N/A'
			currentState['value'] = 'N/A'
			currentState['acceptBal'] = 'N/A'
			currentState['acceptVal'] = 'N/A'
			currentState['mostRecentResponse'] = 'N/A'

			currentState['messagesReceived'] = []
			currentState['blockChain'].append(message['value'])
		else:
			# if transactions are not valid:
			if currentState['proc_num'] == message['sender']:
				trans = currentState['transactions'][:2]
				if validityCheck[0] == False:
					sendRejectTrans(trans[0],NWSock)
					currentState['transactions'].remove(trans[0])

				if validityCheck[1] == False:
					sendRejectTrans(trans[1],NWSock)
					currentState['transactions'].remove(trans[1])


			# if some transactions are invalid:

		# I dont think we need to use this:
		# currentState['BallotNum'] = (len(blockChain), currentState['BallotNum'][1],currentState['proc_num'])


def receiveMessage(message,currentState,NWSock):
	if message['type'] =='prop_ack' and currentState['state'] == 'waiting for prop_ack':
		currentState['messagesReceived'].append(message)
		currentState['mostRecentResponse'] = datetime.datetime.now()
		if len(currentState['messagesReceived']) >= 3:
			sendAccMessages(currentState,NWSock,transactions)
	else:
		if message['type'] == 'acc_ack' and currentState['state'] == 'waiting for acc_ack':
			currentState['messagesReceived'].append(message)
			currentState['mostRecentResponse'] = datetime.datetime.now()

			if len(currentState['messagesReceived']) >= 3:
				sendDecisionMessages(currentState,NWSock,transactions)
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
						receiveDecision(currentState,message,NWSock):
					else: 
						if message['type'] == 'sync':
							sendSyncResponse(currentState,message,NWSock)
						else:
							if message['type'] == 'sync-response':
								for block in message['data']:
									# Test if block is to be the next block in the chain
									if getDepthNumFromBlock(block) == len(currentState['blockChain']) + 1:
										currentState['blockChain'] = currentState['blockChain'].append(block)
							else: 
								if message['type'] == 'transaction':
									currentState['transactions'].append(message['transaction'])
								else:
									if message['type'] == 'print_set':
										sendTransSet(currentState,NWSock)
									else:
										if message['type'] == 'print_balance':
											sendBalance(currentState,NWSock)
										else:
											if message['type'] ==  'print_blockchain':
												sendBlockChain(currentState,NWSock)
	return 0

def initiateCurrentState(proc_num = -25,file=None):
	if file is None:
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

def get_random_string():
	random_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)]) #length of 10
	return random_str


def isValidBlock(block):
	value = hashlib.sha256(block.encode()).hexdigest()
		checker = value[-1]
		# print(value)
		# print(checker)
		if checker.isdigit() == True:
			if int(checker) == 0 or int(checker) == 1:
				return True
			else:
				return False

# TODO for ajit: put in the correct way to access depth number in the block
# Everything in slashes below needs to be replaced with the right thing based on how you organize the data structures
def getDepthNumFromBlock(block):
	return block[/ depth num /]

# TODO for ajit: get the right stuff to access the values
def calculateBalances(currentState):
	currentBalances = initialBalances.copy()
	for block in currentState['blockChain']:
		for transaction in block[/TRANS/]:
			currentBalances[receiver] = currentBalances[/receiver/] + /trans_amnt/
			currentBalances[sender] = currentBalances[/receiver/] - /trans_amnt/
	return currentBalances

#TODO for ajit
def checkIfTransactionsAreValid(currentState,NWSock,transactions):
	bal= calculateBalances(currentState)
	transCorrect = [True,True]
	for trans in [0,1]:
		if bal[/sender/] - transactions[trans][/AMNT/] < 0:
			transCorrect[trans] = False
		else:
			bal[/sender/] = bal[/sender/] - transactions[trans][/AMNT/]
	return transCorrect

#TODO ajit: Create the block from currentState. Everything you need to make it is there. 
# We will only be generating the block once every round until it works. Youll need to calculate hash of previous block and stuff too
def createBlock(currentState):
	# call get_random_string() to generate nonce
	pass		

def transaction_message(networkSocket, client_conn,proc_num):
	
	networkSocket.setblocking(0)
	currentState = initiateCurrentState(proc_num = proc_num)

	lastValidBlock = ''
	
	try:
		while True:
			global clientName
			global serverName
			
			transact_msg = client_conn.recv(1024).decode()
			(sender, receiver, amt) = transact_msg.split()
			currentState['transactions'].append(transact_msg)
			print((sender,receiver,amt))
			print(currentState['transactions'])
			# msg = transactions[0] + get_random_string()
			# value = hashlib.sha256(msg.encode()).hexdigest()
			# print(value)
			# print(type(value))
			# print(value[-1])
			# print(type(value[-1])) #type string

			if(len(currentState['transactions']) > 1):
				#creates block based on current state.
				block = createBlock(currentState)
				if block == lastValidBlock:
					#this means that we have already calculated the right nonce, and because we create block from current state, we know that the block is valid for being the next value
					# so a block hasnt been proposed yet and this block is able to be the next one if paxos is down. 
					pass
				else:
					if isValidBlock(block):
						sendPropMessages(currentState,networkSocket,block)
						lastValidBlock = block
			# receive message and then process if received
			try:
				receivedMessage = networkSocket.recv(1024).decode()
                messageDict = ast.literal_eval(messageString)
                receiveMessage(messageDict,currentState,networkSocket,transactions):


			except socket.error as err:
				pass
			
			#
			if currentState['mostRecentResponse'] != "N/A":
				currentTime = datetime.datetime.now()
				#get time passed since this response
				if (currentTime - currentState['mostRecentResponse']).seconds > timeOutDuration:
					print('Not received any responses to request. Proposition failed. Attempting to update blockChain')
					sendSync(currentState,NWSock)
					lastValidBlock = ''





	finally:
		client_conn.close()




# I dont see there being any depth in your hash here. Im gonna do some reworking
def get_hash(transactions):
	trans_list = []
	trans_list.append(transactions[0])
	trans_list.append(transactions[1])
	temp = True
	while(temp):
		rdstr = get_random_string()
		msg = transactions[0] + transactions[1] + rdstr
		


####### MAIN STARTS HERE
####### ALL HELPER FUNCTIONS GO BEFORE
serverSocket = socket(AF_INET, SOCK_STREAM)
networkSocket = socket(AF_INET, SOCK_STREAM)
transactions = []

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
