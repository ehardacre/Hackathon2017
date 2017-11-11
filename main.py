import server
import time
from multiprocessing import Process

character = 'a'
p = Process(target=server.startServer, args=())
p.start()

while True:
    print character
    time.sleep(.2)
