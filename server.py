import random
import time
import string
import threading
import _thread
from socket import *
import ast
import sys
import hashlib
import config
from socket import error

initialBalances = {'A': 100, 'B': 100, 'C': 100, 'D': 100, 'E': 100}
timeOutDuration = 15

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
			if balGreaterThanOrEqual(message['acceptBal'],b):
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
	NWSock.send(bytes(str(newMessage) , encoding='utf8'))


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
		validityCheck = checkIfTransactionsAreValid(currentState,NWSock)
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
		print('Received prop_ack')
		currentState['messagesReceived'].append(message)
		currentState['mostRecentResponse'] = datetime.datetime.now()
		if len(currentState['messagesReceived']) >= 3:
			sendAccMessages(currentState,NWSock,transactions)
	else:
		if message['type'] == 'acc_ack' and currentState['state'] == 'waiting for acc_ack':
			print('Received acc_ack')
			currentState['messagesReceived'].append(message)
			currentState['mostRecentResponse'] = datetime.datetime.now()

			if len(currentState['messagesReceived']) >= 3:
				sendDecisionMessages(currentState,NWSock,transactions)
		else:
			if message['type'] == 'prop':
				print('Received prop')
				if balGreaterThanOrEqual(message['bal'],currentState['BallotNum']):
					currentState['BallotNum'] = message['bal']
					sendPropAck(message,currentState,NWSock)
			else:
				if message['type'] == 'acc':
					print('Received acc')
					if balGreaterThanOrEqual(message['bal'],currentState['BallotNum']):
						currentState['acceptBal']=message['bal']
						currentState['acceptVal'] = message['value']
						sendAccAck(message,NWSock)
				else:
					if message['type'] == 'decision':
						print('Received decision')
						receiveDecision(currentState,message,NWSock)
					else:
						if message['type'] == 'sync':
							print('Received request to sync')
							sendSyncResponse(currentState,message,NWSock)
						else:
							if message['type'] == 'sync-response':
								print('Received data from another server')
								for block in message['data']:
									# Test if block is to be the next block in the chain
									if getDepthNumFromBlock(block) == len(currentState['blockChain']) + 1:
										currentState['blockChain'] = currentState['blockChain'].append(block)
							else:
								if message['type'] == 'transaction':
									print('Received transaction request from client')
									currentState['transactions'].append(message['transaction'])
									print('Transaction List is now: ' + str(currentState['transactions']))
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

#added blockChain field for initialization
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
		currentState['transactions'] = []
		currentState['blockChain'] = []
	return currentState

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
	return block[0][0]

# TODO for ajit: get the right stuff to access the values
def calculateBalances(currentState):
	currentBalances = initialBalances.copy()
	for block in currentState['blockChain']:
		for transaction in block[1]:
			try:
				(sender, receiver, amt) = transaction.split()
				currentBalances[receiver] = currentBalances[receiver] + amt
				currentBalances[sender] = currentBalances[receiver] - amt
			except ValueError:
				print("not a transaction")

	return currentBalances

#TODO for ajit
#do we want to return bal as well?
def checkIfTransactionsAreValid(currentState,NWSock):
	trans = currentState['transactions'][:2]
	bal= calculateBalances(currentState)
	transCorrect = [True,True]
	for transact in trans:
		(sender, rec, amt) = transact.split()
		if bal[sender] - amt < 0:
			transCorrect[trans] = False
		else:
			bal[sender] = bal[sender] - amt
	return transCorrect

#TODO ajit: Create the block from currentState. Everything you need to make it is there.
# We will only be generating the block once every round until it works. Youll need to calculate hash of previous block and stuff too
def createBlock(currentState):
	# call get_random_string() to generate nonce
	transactions = currentState['transactions'][:2]
	blockChain = currentState['blockChain']
	nonce = get_random_string()
	depth_newblock = len(blockChain) + 1
	string_to_hash = transactions[0] + transactions[1] + nonce
	hash_value = hashlib.sha256(string_to_hash.encode()).hexdigest()
	if depth_newblock == 1:
		prev_hash = "NULL"
	else:
		prev_transaction_1 = blockChain[len(blockChain)-1][1][0]
		prev_transaction_2 = blockChain[len(blockChain)-1][1][1]
		prev_depth = blockChain[len(blockChain)-1][0][0]
		hash_prev = blockChain[len(blockChain)-1][0][1]
		prev_nonce = blockChain[len(blockChain)-1][0][2]
		string_hash =  prev_transaction_1 + prev_transaction_2 + str(prev_depth) + hash_prev + prev_nonce
		prev_hash = hashlib.sha256(string_hash.encode()).hexdigest()

	head_of_block = (depth_newblock, prev_hash, nonce)
	transactions_in_block = []
	transactions_in_block.append(transactions[0])
	transactions_in_block.append(transactions[1])
	block = (head_of_block, transactions_in_block)
	return block

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

def validHash(transaction_list, nonce, string_to_hash, hash_value):
	if(hash_value[-1] != 0 or hash_value[-1] != 1):
		nonce = get_random_string()
		msg = transaction_list[0] + transaction_list[1] + nonce
		hash = hashlib.sha256(msg.encode()).hexdigest()
		return False, hash
	elif(hash_value[-1] == 0 or hash_value[-1] == 1):
		return True, hash_value

def run(proc_num):

	currentState = initiateCurrentState(proc_num = proc_num)

	lastValidBlock = ''

	NWSock = connectToNetwork(currentState['proc_num'])
	print('NW Connected')

	try:
		while True:
			messageString = ''
			try:
				messageString = NWSock.recv(1024).decode('utf-8')

			except:
				pass

			if messageString != '':

				messageDict = ast.literal_eval(messageString)
				print('Received message' + str(messageDict))
				receiveMessage(messageDict,currentState,NWSock)


			# if currentState['mostRecentResponse'] != "N/A":
			# 	currentTime = datetime.datetime.now()
			# 	#get time passed since this response
			# 	if (currentTime - currentState['mostRecentResponse']).seconds > timeOutDuration:
			# 		print('Not received any responses to request. Proposition failed. Attempting to update blockChain')
			# 		sendSync(currentState,NWSock)
			# 		lastValidBlock = ''


			# if(len(currentState['transactions']) > 1):
			# 	#creates block based on current state.
			# 	block = createBlock(currentState)
			# 	if block == lastValidBlock:
			# 		#this means that we have already calculated the right nonce, and because we create block from current state, we know that the block is valid for being the next value
			# 		# so a block hasnt been proposed yet and this block is able to be the next one if paxos is down.
			# 		pass
			# 	else:
			# 		if isValidBlock(block):
			# 			sendPropMessages(currentState,NWSock,block)
			# 			lastValidBlock = block
			# # receive message and then process if received


			# except socket.error as err:
			# 	pass
			#
			# #
			# if currentState['mostRecentResponse'] != "N/A":
			# 	currentTime = datetime.datetime.now()
			# 	#get time passed since this response
			# 	if (currentTime - currentState['mostRecentResponse']).seconds > timeOutDuration:
			# 		print('Not received any responses to request. Proposition failed. Attempting to update blockChain')
			# 		sendSync(currentState,NWSock)
			# 		lastValidBlock = ''

	except:
		pass
### MAIN STARTS HERE

run(proc_num = int(sys.argv[1]))
