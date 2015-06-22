#!/usr/bin/python 
import socket, select, string, sys

def prompt():
	sys.stdout.write('<%s>' % name)
	sys.stdout.flush()

name = raw_input("Enter username: ")
if len(sys.argv) < 3 :
	print 'Usage: python chatclient.py [hostname] [port]'
	sys.exit()
host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2) 

try:
	s.connect((host, port))
except:
	print 'Unable to connect. Exiting.'
	sys.exit()

print 'Connected to remote host.'
prompt()

while 1:
	socket_list = [sys.stdin, s]
	read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
	for sock in read_sockets:
		if sock == s :
			data = sock.recv(4096)
			if not data:
				print('\nDisconnected from chat server. Exiting.')
				sys.exit()
			else:
				sys.stdout.write(data)
				prompt()
		else:
			msg = sys.stdin.readline()
			s.send(msg)
			prompt()

