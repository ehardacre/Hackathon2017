import socket

UDP_IP_ADRESS = '10.130.7.43'
UDP_PORT_NO = 8909

Message = "Hello, World"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(Message, (UDP_IP_ADRESS, UDP_PORT_NO))
