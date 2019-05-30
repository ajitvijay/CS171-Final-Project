
def balGreaterThanOrEqual(bal,ballotNum):
	pass

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

def sendAccMessages(messagesReceived,NWSock):
	value = None
	b = None
	for message in messagesReceived:
		if message['value'] is not None:
			if balGreaterThanOrEqual(message['bal'],b)
				value = message['value']
				b =
	newMessage = {}
	newMessage ['type'] = 'acc'
	newMessage ['type'] = ''

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
				if balGreaterThanOrEqual(message['bal'],currentState['ballotNum']):
					currentState['ballotNum'] = message['bal']
					sendPropAck(message,currentState,NWSock)
			else:
				if message['type'] == 'acc':
					if balGreaterThanOrEqual(message['bal'],currentState['ballotNum']):
						currentState['acceptBal']=message['bal']
						currentState['acceptVal'] = message['value']
						sendAccAck(message,NWSock)
				else:
					if message['type'] == 'decision':
						messagesReceived = []
						currentState['state'] = 'decided'
						currentState['acceptVal'] = message['value']
						currentState['acceptBal'] = message['bal']
						#in code after this function, currentState['acceptVal'] will be added to block chain
