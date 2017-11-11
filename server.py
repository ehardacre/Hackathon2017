# import socket, pygame
# from pygame.locals import *
#
# UDP_IP_ADRESS = '10.130.7.43'
# UDP_PORT_NO = 8909
# serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serverSock.bind((UDP_IP_ADRESS,UDP_PORT_NO))
#
# WINDOW_WIDTH = 500
# WINDOW_HEIGHT = 500
#
# def main():
#     pygame.init()
#     DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     FONT = pygame.font.SysFont('Courier.ttf',20)
#     text, textRect = makeTextObjs("TYPE TO BEGIN", FONT, (255, 255, 255))
#     textRect.center = (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
#     DISPLAY.blit(text, textRect)
#     pygame.display.update()
#     done = False
#     while not done:
#         data, addr = serverSock.recvfrom(1024)
#         print("Message: " + data)
#         DISPLAY.fill((0,0,0))
#         text, textRect = makeTextObjs(data, FONT, (255, 255, 255))
#         textRect.center = (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2))
#         DISPLAY.blit(text, textRect)
#         pygame.display.update()
#
#
# def makeTextObjs(text, font, color):
#     surf = font.render(text, True, color)
#     return surf, surf.get_rect()
#
# main()


import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print "received message:", data
