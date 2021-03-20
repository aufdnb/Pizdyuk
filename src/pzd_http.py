import json
import market.user_manager as user_manager
import market.trader as trader
from http.server import BaseHTTPRequestHandler, HTTPServer
from pzd_threading import Pizdyuk_Thread

class PizdyukRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, response=None):
        response = json.dumps(response)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        get_data = self.rfile.read(content_length).decode('utf-8')
        self._set_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = json.loads(post_data)
        response = self.__handle_request(post_data)
        self._set_response(response)

    def __handle_request(self, post_data):
        action = post_data.get("action", None)

        if not action:
            return

        t = trader.get_trader()
        manager = user_manager.get_manager()
        action.lower()

        response = {}

        if action == "buy" or action == "sell":
            response = t.handle_order(action, **post_data)
        elif action == "create_user":
            response = manager.handle_create_request(**post_data)

        return response

    def __validate_data(self, data):
        pass


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
        thread.on_error.add_handler(lambda e: print("ERROR {}".format(e)))
        thread.start()

    def close(self):
        self.__server.shutdown()

    @property
    def port(self):
        return self.__port

    @property
    def server_address(self):
        return self.__server_address