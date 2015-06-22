#!/usr/bin/python 
import socket
import select

def broadcast_data (sock, message):
	for socket in CONNECTION_LIST:
		if socket!= server_socket and socket!=sock:
			try:
				socket.send(message)
			except:
				socket.close()
				CONNECTION_LIST.remove(socket)
CONNECTION_LIST = []
RECV_BUFFER = 4096
PORT = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(5)
CONNECTION_LIST.append(server_socket)

print "Chat server started on port " + str(PORT)
	
while 1:
	read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST, [],[])
	for sock in read_sockets:
		if sock == server_socket:
			sockfd, addr = server_socket.accept()
			CONNECTION_LIST.append(sockfd)
			print "Client (%s, %s) connected" %addr
			broadcast_data(sockfd, "[%s,%s] entered room\n" %addr)
		else:
			data = sock.recv(RECV_BUFFER)
			if data:
				broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '>' + data)
			else:
				broadcast_data(sock, "Client (%s, %s) is offline" %addr)
				print "Client (%s, %s) is offline" %addr
				sock.close()
				CONNECTION_LIST.remove(sock)
server_socket.close()
