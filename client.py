import socket


host = '172.20.10.3'
port = 5009
Message = "Hello, World"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.connect((host,port))

while True:
    userInput = raw_input("Enter a command: ")
    clientSock.send(userInput.encode('utf-8'))


# Kevin's IP information for connecting to his Mac
# host = '10.130.6.38'
# port = 5006
