from http.server import BaseHTTPRequestHandler, HTTPServer
from pzd_threading import Pizdyuk_Thread

class PizdyukRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("Get request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


class PizdyukServer:
    """ HTTPServer wrapper class """
    def __init__(self, server_address, handler, port=8080):
        self.__handler = handler
        self.__port = port
        self.__server_address = server_address
        self.__server = HTTPServer((server_address, port), handler)
        self.__server

    def start(self):
        thread = Pizdyuk_Thread(self.__server.serve_forever)
        thread.on_started.add_handler(lambda: print("Thread started on {0}:{1}".format(self.server_address, self.port)))
        thread.start()

    def close(self):
        self.__server.shutdown()

    @property
    def port(self):
        return self.__port

    @property
    def server_address(self):
        return self.__server_address