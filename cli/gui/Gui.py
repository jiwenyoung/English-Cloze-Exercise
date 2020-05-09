import socketserver, json, time
import socket
from .Hub import Hub
from .Handler import Handler

class View:
    def red(self, text):
        print(f"\033[1;31m{text}\033[0m")
        return self

class MyTCPHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.connection = self.request

    def handle(self):
        view = View()
        try:
            connection = self.connection
            data = connection.recv(4096).strip()
            data = json.loads(data)
            name = data["name"]
            arguments = data["arguments"]
            handler = Hub(Handler)
            if handler.is_yield_function(name):
                for item in handler.register(name).generate(arguments):
                    response = json.dumps(item)
                    time.sleep(0.03)
                    connection.sendall(bytes(response, encoding="utf-8"))
            else:
                response = handler.register(name).run(arguments)
                response = json.dumps(response)
                connection.sendall(bytes(response, encoding="utf-8"))
        except Exception as error:
            raise error
            view.red(error)

class Gui:
    def run(self):
        HOST, PORT = "localhost", 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server.socket.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,True)
            server.serve_forever()