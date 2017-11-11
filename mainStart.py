import time
import socket
import pyautogui
from multiprocessing import Process, Value

class Server:
    def __init__(self):
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 6969
        print "UDP target IP:", self.UDP_IP
        print "UDP target port:", self.UDP_PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

    def startServer(self, command, entered):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print "received message: ", data
            command.value = data
            entered.value = 1


def parseCommand(command):
    if command == "l":
        print "Turned left."
        pyautogui.press('q')
    elif command == "r":
        print "Turned right"
        pyautogui.press('w')
    elif command == "a":
        print "Moved left."
        pyautogui.press('a')
    elif command == "d":
        print "Moved right."
        pyautogui.press('d')
    elif command == "s":
        print "Dropped down."
        pyautogui.press('space')
    else:
        print "Not recognized."

def checkForCommand():
    return commandInputted.value == 1

def initServer():
    global commandInputted
    global character
    server = Server()
    commandInputted = Value('i', 0)
    character = Value('c', "x")
    p = Process(target=server.startServer, args=(character,commandInputted,))
    p.start()

# while True:
#     if checkForCommand():
#         parseCommand(character.value)
#         commandInputted.value = 0
