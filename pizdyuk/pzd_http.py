import json
import market.user_manager as users
import market.stock_manager as stocks
import market.trader as trader
from http.server import BaseHTTPRequestHandler, HTTPServer
from pzd_threading import Pizdyuk_Thread
from pzd_logging import PizdyukLogger

class PizdyukRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, response):
        """ 
            Parses the passed response and writes the contents to wfile

            Args:
            response (Tuple[int, dict[str, str]]) - where int is the status code amd dict is the contents of the response
        """
        status_code = response[0]
        msg = response[1]
        msg = json.dumps(msg)
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(msg.encode('utf-8'))

    def do_GET(self):
        """
            Handles a GET request
        """
        content_length = int(self.headers['Content-Length'])
        get_data = self.rfile.read(content_length).decode('utf-8')
        get_data = json.loads(get_data)
        response = self.__handle_request("get", get_data)
        self._set_response(response)

    def do_POST(self):
        """
            Handles a POST request
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = json.loads(post_data)
        response = self.__handle_request("post", post_data)
        self._set_response(response)

    def __handle_request(self, request_type, request_data):
        response = None
        request_type = request_type.lower()
        switch = {
            "post": self.__handle_post_request,
            "get": self.__handle_get_request,
        }

        try:
            response = switch[request_type](request_data)
        except Exception as e:
            PizdyukLogger.get_logger().log_error(str(e))
            return (500, {"error": "Uknown error ocurred"})

        return response

    def __handle_post_request(self, post_data):
        action = post_data.get("action", None)

        if not action:
            return (400, {"error": "Missing 'action' field."})

        response = (400, {"error": "Invalid request"})
        t = trader.get_trader()
        user_manager = users.get_manager()
        action.lower()

        response = {}

        if action == "buy" or action == "sell":
            response = t.handle_order(action, **post_data)
        elif action == "create_user":
            response = user_manager.handle_create_request(**post_data)
        elif action == "add_funds":
            response = user_manager.handle_add_funds_request(**post_data)

        return response

    def __handle_get_request(self, get_data):
        action = get_data.get("action", None)
        response = (400, {"error": "Invalid request"})

        if not action:
            return (400, {"error": "Missing 'action' field."})

        stock_manager = stocks.get_manager()
        user_manager = users.get_manager()

        if action == "get_stock":
            response = stock_manager.handle_request(**get_data)
        elif action == "get_user":
            response = user_manager.handle_get_request(**get_data)

        return response


class PizdyukServer:
    """ HTTPServer wrapper class """
    def __init__(self, server_address, handler, port=8080):
        """
            PizdyukServer constructor

            Args:
            server_address (str) - server url
            handler (BaseHTTPRequestHandler) - http handler
            port [Optional] (int) - target port for listening
        """
        self.__handler = handler
        self.__port = port
        self.__server_address = server_address
        self.__server = HTTPServer((server_address, port), handler)
        self.__logger = PizdyukLogger.get_logger()
        self.__is_running = False

    def start(self):
        """
            If not started, starts a server on a separate thread.
        """
        if self.__is_running:
            return

        thread = Pizdyuk_Thread(self.__server.serve_forever)
        thread.on_started.add_handler(lambda: self.__logger.log_info("Thread started on {0}:{1}".format(self.server_address, self.port)))
        thread.on_error.add_handler(lambda e: self.__logger.log_error(str(e)))
        thread.start()
        self.__is_running = True

    def close(self):
        """
            If running, shutdowns the server,
        """
        if not self.__is_running:
            return

        self.__logger.log_info("Closing the server on {0}:{1}".format(self.__server_address, self.__port))
        self.__server.shutdown()
        self.__is_running = False

    @property
    def port(self):
        """
            The getter for 'port' property
        """
        return self.__port

    @property
    def server_address(self):
        """
            The getter for 'server_address' property
        """
        return self.__server_address

    @property
    def is_running(self):
        """
            The getter for 'is_running' property
        """
        return self.__is_running