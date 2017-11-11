import socket

host = '127.0.0.1'
port = 5100

Message = "Hello, World"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect((host,port))

while True:
    userInput = raw_input("Enter a command: ")
    clientSock.send(userInput.encode('utf-8'))
