import socket
from time import sleep
from time import time

host = '134.173.87.133'
port = 5809
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def sendPic(s, filePath):
    print(filePath)
    pic = open(filePath, 'rb')
    chunk = pic.read(1024)
    s.send(str.encode("STORE " + filePath))
    t = time()
    while chunk:
        print("Sending Picture")
        s.send(chunk)
        chunk = pic.read(1024)
    pic.close()
    print("Done sending")
    print("Elapsed time = " + str(time() - t) + 's')
    s.close()
    return "Done sending"

def sendReceive(s, message):
    s.send(str.encode(message))
    reply = s.recv(1024)
    print("We have received a reply")
    print("Send closing message.")
    s.send(str.encode("EXIT"))
    s.close()
    reply = reply.decode('utf-8')
    return reply

def transmit(message):
    s = setupSocket()
    response = sendReceive(s, message)
    return response

def backup(filePath):
    s = setupSocket()
    response = sendPic(s, filePath)
    return response
    
s = setupSocket()

while True: 
	command = input("Enter your command: ")
	if command == 'EXIT':
		s.send(str.encode(command))
		break
	elif command == 'KILL':
		s.send(str.encode(command))
		break
	s.send(str.encode(command))
	reply = s.recv(1024)
	print(reply.decode('utf-8'))
	
s.close()