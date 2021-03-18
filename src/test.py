import time
from pzd_http import PizdyukServer, PizdyukRequestHandler

server = PizdyukServer("localhost", PizdyukRequestHandler)
server.start()

time.sleep(5)

server.close()