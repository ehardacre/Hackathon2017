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
    if command == "q":
        print "Turned left for P1."
        pyautogui.press('q')
    elif command == "e":
        print "Turned right for P1"
        pyautogui.press('e')
    elif command == "a":
        print "Moved left for P1."
        pyautogui.press('a')
    elif command == "d":
        print "Moved right for P1."
        pyautogui.press('d')
    elif command == "w":
        print "Dropped down for P1."
        pyautogui.press('w')
    elif command == "u":
        print "Turned left for P2."
        pyautogui.press('u')
    elif command == "o":
        print "Turned right for P2"
        pyautogui.press('o')
    elif command == "j":
        print "Moved left for P2."
        pyautogui.press('j')
    elif command == "l":
        print "Moved right for P2."
        pyautogui.press('l')
    elif command == "i":
        print "Dropped down for P2."
        pyautogui.press('i')
    elif command == "1":
        print "P1 Connected."
        pyautogui.press('1')
    elif command == "2":
        print "P2 Connected."
        pyautogui.press('2')
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
