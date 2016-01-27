# Distributed Systems Project
# Exercise 1: Vector Clock (vector.py)
# Ilkka Lehikoinen
# 013787637

#!/usr/bin/python

import sys
import socket
import select
import random
import re

# Global variables

index=0
ids={}
hosts={}
ports={}
vector={}

# socket for sending a vector
def client(hostTo, portTo, sendVector):
	s = socket.socket()         # Create a socket object
	host = hostTo 	
	port = int(portTo) 		
	
# vector message format [ 1 2 3 4 5 ]
	sendData="[ "+" ".join("{0}".format(n) for n in sendVector.values())+" ]"

	try:
		s.connect((host, port))
	except socket.error, exc:
		pass # print "Caught exception socket.error : %s" % exc
	else:
		s.send(sendData)
		s.close                     # Close the socket when done

# local event increases local clock randomly 
def localEvent():
	increased=random.randint(1, 5)
	print "l", increased
	return increased

# send message selects random host
def sendMessage(sendVector):

# makes sure that dont send to itself
	while True:
		nodeId = random.randint(1, index)
		if nodeId!=myId:
			break
	toNode = hosts[nodeId]
	toPort = ports[nodeId]

	#Send
 	client(toNode, toPort, sendVector)

	print "s", toNode, "["," ".join("{0}".format(n) for n in sendVector.values()),"]"

# receive message 
def recvMessage(sender, recvVector, localVector):
# compares vectors and updates
	for i in range(1, len(localVector)+1):
		if localVector[i]<int(recvVector[i-1]):
			localVector[i]=int(recvVector[i-1])

	print "r", sender,"["," ".join("{0}".format(n) for n in recvVector),"] ["," ".join("{0}".format(n) for n in localVector.values()),"]"

# Main program

if len(sys.argv)<3:
	print "Too few arguments"
	sys.exit(2) 

configurationFile = sys.argv[1]
myId = int(sys.argv[2])

# open file
f=open(configurationFile, 'r')
for line in f:
	index +=1
	# creates separates tables for ids, hosts and ports
	ids[index]=line.split(" ")[0]
	hosts[index]=line.split(" ")[1]
	ports[index]=line.split(" ")[2]
	# initializes the vector clock
	vector[index]=0

# Server socket creation
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name

# checks that is the same hosts as indicated by configuration_file id
if host!=hosts[myId]:
	print host, "is not", hosts[myId]
	sys.exit(2)

port = int(ports[myId])     # Reserve a port for your service.

s.bind((host, port))        # Bind to the port
# Making socket to be non-blocking
s.setblocking(0)
s.listen(5)                 # Now wait for client connection.
s.settimeout(1)				# delay waiting socket

input = [s]

# Main loop should end when vector[myId]>=100
while vector[myId]<100:
	try:
		c, addr = s.accept()     # Establish connection with client.
	except socket.error:
		pass
	else:
# buffer (1000) should be scaled along with the vector (# of nodes)
		data=c.recv(1000)		
		c.close()
		recvVector=data.replace('[ ','').replace(' ]','').split()
		# increases local clock by 1
		vector[myId] += 1
		# handles the received vector
		recvMessage(addr[0], recvVector, vector)

	# randomly chooses local event or send event
	if random.randint(1,2)==1:
		vector[myId] += localEvent()
	else:
		vector[myId] += 1
		sendMessage(vector)

