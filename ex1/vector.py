# Distributed Systems Project
# Exercise 1: Vector Clock (vector.py)
# Ilkka Lehikoinen
# 013787637

#!/usr/bin/python

import sys
import socket
import select
import random

# Global variables

index=0
ids={}
hosts={}
ports={}
vector={}

def client(hostTo, portTo, sendVector):
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 34568                # Reserve a port for your service.	

	s.connect((host, port))
	print s.recv(1024)
	s.close                     # Close the socket when done

def localEvent():
	increased=random.randint(1,5)
	print "l", increased
	return increased

def sendMessage(sendVector):
	nodeId = random.randint(1, index)
	toNode = hosts[nodeId]
	toPort = ports[nodeId]
#Send
# 	client(toNode, toPort, sendVector)

	print "s", toNode, "["," ".join("{0}".format(n) for n in sendVector.values()),"]"

def recvMessage(sender, recvVector, localVector):
	
	print "r", sender,"["," ".join("{0}".format(n) for n in recvVector),"] ["," ".join("{0}".format(n) for n in localVector),"]"

# Main program

if len(sys.argv)<3:
	print "Too few arguments"
	sys.exit(2) 

configurationFile = sys.argv[1]
myId = int(sys.argv[2])

f=open(configurationFile, 'r')
for line in f:
	index +=1
#	print line
	ids[index]=line.split(" ")[0]
	hosts[index]=line.split(" ")[1]
	ports[index]=line.split(" ")[2]
	vector[index]=0

# DEBUGGING
# print ids[1]
# print hosts[3]
# print ports[4]
# print index
# print hosts

# print configurationFile
# print myId
vector[myId] += localEvent()
# print vector[myId]
sendMessage(vector)
recvMessage("ukko123", vector, vector)


# Server socket creation
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
print host
# NOTE! Should check that the local machine is same as intented host
port = 34567                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
# Making socket to be non-blocking
s.setblocking(0)
s.listen(5)                 # Now wait for client connection.
s.settimeout(1)
#
input = [s]


# Main loop should end when vector[myId]>=100
while True:
	try:
		c, addr = s.accept()     # Establish connection with client.
	except socket.error:
		pass
	else:
		print 'Got connection from', addr[0]
		data=c.recv(100).split(" ")
		for vectorValue in data:
			print vectorValue
		recvMessage(addr[0], data, vector)	

#	print c
#	print 'Got connection from'  #, addr
#	c.send('Thank you for connecting')
#	c.close()                # Close the connection

	if random.randint(1,2)==1:
		vector[myId] += localEvent()
	else:
		vector[myId] += 1
		sendMessage(vector)

'''
        input_ready,output_ready,errors = select.select(input, [], [])
       
        for sock in input_ready:
            if sock is s:
                client,address = sock.accept()
                print "Accepting socket from",address[0]
                input.append(client)
            else:
                data = sock.recv(1024)
                if data:
                    print data
                else:
                    sock.close()
                    input.remove(sock)
                    print "Dropped connection",address[0]
'''
