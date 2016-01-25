# Distributed Systems Project
# Exercise 1: Vector Clock
# Ilkka Lehikoinen
# 013787637


# Server Example

#!/usr/bin/python           # This is server.py file

import sys
import socket               # Import socket module

def localEvent(increased):
	print "l", increased

def sendMessage(toNode, vector):
	print "s", toNode, "[",vector,"]"

def recvMessage():
	print "r s [t] [n]"

print 'Number of Arguments: ', len(sys.argv), 'arguments.'
print 'Argument List: ', str(sys.argv)

if len(sys.argv)<3:
	print "Too few arguments"
	sys.exit(2) 

configurationFile = sys.argv[1]
lineNumber = int(sys.argv[2])
print configurationFile
print lineNumber

localEvent(lineNumber)
sendMessage("ukko344", lineNumber)

f=open(configurationFile, 'r')
for line in f:
	print line

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   c.send('Thank you for connecting')
   c.close()                # Close the connection


# Client Example

#!/usr/bin/python           # This is client.py file
'''
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
s.close                     # Close the socket when done
'''
