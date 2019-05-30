<<<<<<< HEAD

=======
>>>>>>> e919842f9548b7df50e2e14591f224ef9b9cd151
def balGreaterThanOrEqual(bal,ballotNum):
	if bal[0] > ballotNum[0]
		return True
	else:
		if bal[0] == ballotNum[0] and bal[1] > ballotNum[1]:
			return True
		else:
			if bal[0] == ballotNum[0] and bal[1]== ballotNum[1]:
				return bal[2] >= ballotNum[2]

def sendPropAck(message,currentState,NWSock)
	newMessage = {}
	newMessage['type'] = 'prop_ack'
	newMessage['bal'] = message['bal']
	newMessage['acceptBal'] = currentState['acceptBal']
	newMessage['acceptVal'] = currentState['acceptVal']
	newMessage['destination'] = message['sender']
	newMessage['sender'] = message['destination']
    NWSock.send(bytes(str(newMessage) + '%', encoding='utf8'))


def sendAccAck(message,NWSock):
	newMessage = {}
	newMessage['type'] = 'acc_ack'
	newMessage['bal'] = message['bal']
	newMessage['value'] = message['value']
	newMessage['destination'] = message['sender']
	newMessage['sender'] = message['destination']
    NWSock.send(bytes(str(newMessage) + '%', encoding='utf8'))

def sendPropMessages(currentState,NWSock,newBlock):
	newMessage = {}
	newMessage['type'] = 'prop'
	newMessage['bal'] = (newBlock['depth'],currentState['BallotNum'][1]+1,currentState['proc_num'])
	newMessage['sender'] = currentState['proc_num']
	messagesReceived = []
	currentState['state'] = 'waiting for prop_ack'
	for server in [0,1,2,3,4]:
		newMessage['destination'] = server
		if newMessage['destination'] == newMessage['sender']:
			receiveMessage(message,currentState,messagesReceived,NWSock)
	    else:
	    	NWSock.send(bytes(str(newMessage) + '%', encoding='utf8'))

def sendAccMessages(messagesReceived,currentState,NWSock):
	value = None
	b = None
	for message in messagesReceived:
		if message['value'] is not None:
			if balGreaterThanOrEqual(message['bal'],b)
				value = message['value']
				b =
	newMessage = {}
	newMessage ['type'] = 'acc'
	newMessage ['bal'] = messagesReceived[0]['bal']
	if value is not None:
		newMessage['value'] = value
	else:
		newMessage['value'] = currentState['value']
	newMessage['sender'] = messagesReceived[0]['destination']

	messagesReceived = []
	currentState['state'] = 'waiting for acc_ack'

def receiveMessage(message,currentState,messagesReceived,NWSock):
	if message['type'] =='prop_ack' and currentState['state'] == 'waiting for prop_ack':
		messagesReceived.append(message)
		if len(messagesReceived) >= 3:
			sendAccMessages(messagesReceived)
	else:
		if message['type'] == 'acc_ack' and currentState['state'] == 'waiting for acc_ack':
			messagesReceived.append(message)
			if len(messagesReceived) >= 3:
				sendDecisionMessages(messagesReceived)
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
						messagesReceived = []
						currentState['state'] = 'N/A'
						currentState['value'] = 'N/A'
						currentState['acceptBal'] = 'N/A'
						currentState['acceptVal'] = 'N/A'

						blockChain.append(message['value'])

						currentState['BallotNum'] = (len(blockChain), currentState['BallotNum'][1],currentState['proc_num'])


def separateMessages(message):
    remainingMessage = message
    messageStrings = []
    while len(remainingMessage) > 3:
        messageStrings.append(remainingMessage[:remainingMessage.find('%')])
        if len(remainingMessage[remainingMessage.find('%'):]) > 3:
            remainingMessage = remainingMessage[remainingMessage.find('%') + 1:]
        else:
            remainingMessage = ''
    return messageStrings

def readConfigFile(configFile):
	with open(configFile, “r”) as f:
		lines = f.readlines()
		return str(lines[-1])


def run(proc_num,NWconfigFile):
	blockChain = []

	messagesReceived = []
	currentState = {}
	currentState['state']= 'N/A'
	currentState['acceptVal']= 'N/A'
	currentState['acceptBal']= 'N/A'
	#is default value for when a block is successfully mined:
	currentState['value']= 'N/A'
	currentState['BallotNum']= (0,0,proc_num)
	currentState['proc_num']= proc_num

	networkPort = readConfigFile(NWconfigFile)
	try:
	    nwSock.connect(('127.0.0.1', networkPort))

	while True:
        time.sleep(1)

        try:
            client, addr = clientSock.accept()
            print('Got connection with client at ', addr)
            client.setblocking(0)

        except socket.error as err:
            pass

        # manage sending a message when received one from client
        try:
            if client is not None:
                messageString = client.recv(1024).decode('utf-8')

                if messageString != '':
                    print("Received transaction request from client ")
                    messageDict = ast.literal_eval(str(messageString))
                    #include trans code here

        except socket.error as err:
            pass

        # Manage receiving a message from the network
        try:
            if nwSock is not None:
                messageString = nwSock.recv(1024).decode('utf-8')

                if messageString != '':
                    messageStrings = separateMessages(messageString)

                    for message in messageStrings:
                        messageDict = ast.literal_eval(str(message))
                        receiveMessage(messageDict, currentState,messagesReceived, nwSock)

        except socket.error as err:
            pass
