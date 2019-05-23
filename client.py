import random
import socket
import threading
import time
import ast



def bindServer(startingPort,procNum,configFile):
	connect = False
	while not connect:
		try:

		    connection = serverListener.bind(('', startingPort))
			connect = True
		except socket.error as err:
			startingPort = startingPort + 1
			pass
	#read the dict, add new port number to it
	configDict = {}
	with open(configFile, "r") as config:
        lineList = myfile.readlines()
	    configDict = ast.literal_eval(str(lineList[-1]))
	    configDict[str(procNum)] = startingPort
	# add updated dict to config
	with open(configFile,"w") as config:
		config,write(str(configDict))
	return connection

#will be run concurrently to connectToLessThanServers. End result is two dicts that are combined.
def waitToReceiveConnections(portNum,procNum,maxProc):
	receivedCount = 0
	connections = {}
	while receivedCount < maxProc - procNum:
	    sock,addr = serverListener.accept()
	    procID = sock.recv(1024).decode('utf-8')
	    connections[str(procID)] = sock
	return connections	

def connectToLessThanServers(procNum,ports):
	connections = {}

	for proc in range(procNum-1,1):
		    connections[str(proc)] = sock.connect(('127.0.0.1', ports[str(proc)]))
			connections[str(proc)].send(bytes(procNum))
	return connections