import random
from socket import *
import socket
import time
import threading
import _thread
import ast
import hashlib

def sendMessageWithDelay(message, destination,destinationInt):
    sleepAmnt = random.uniform(0, 3)
    print('Sending message: ' + str (message))
    if int(destinationInt) >0:
        time.sleep(sleepAmnt)
    destination.send(bytes(message + '%',encoding='utf-8'))

def separateMessages(message):
    remainingMessage = message
    messageStrings = []
    while len(remainingMessage) > 3:
        messageStrings.append(remainingMessage[:remainingMessage.find('%')])
        if len(remainingMessage[remainingMessage.find('%') :]) > 3:
            remainingMessage = remainingMessage[remainingMessage.find('%') + 1:]
        else:
            remainingMessage = ''
    return messageStrings



def bindSocketAndSave():
    serverPortNumber = 3456

    serverListener = socket.socket()

    while True:

        try:
            serverListener.bind(('', serverPortNumber))
            break
        except:
            serverPortNumber = serverPortNumber + 1
            pass
    print('Bound on port: ' + str(serverPortNumber))
    with open('config.py', 'w') as f:
        f.write('serverPortNumber =' + str(serverPortNumber))

    serverListener.listen(5)
    serverListener.setblocking(0)

    return serverListener


def startNetwork():

    serverListener = bindSocketAndSave()

    serverSockets = {}

    while True:
        # Try to accept other server connections
        try:

            sock, addr1 = serverListener.accept()
            procID = sock.recv(1024).decode('utf-8')

            print('Started connection with server: ' + procID)

            sock.setblocking(0)
            serverSockets[procID] = sock
        except socket.error as err:
            pass

# Send messages with delay
        for socketVar in serverSockets.values():
            try:
                messageString = socketVar.recv(1024).decode('utf-8')

                if messageString != '':
                    messages = separateMessages(messageString)
                    for message in messages:
                        print('Received message: ' + message)

                        messageDict = ast.literal_eval(message)

                        sendThread = threading.Thread(target=sendMessageWithDelay, args=(message, serverSockets[str(messageDict['destination'])],messageDict['destination']) )
                        sendThread.start()

            except socket.error as err:
                pass

startNetwork()
