import socketserver, json
from .Hub import Hub
from .Handler import Handler

class View:
    def red(self, text):
        print(f"\033[1;31m{text}\033[0m")
        return self

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        view = View()
        try:
            socket = self.request
            data = socket.recv(4096).strip()
            data = json.loads(data)
            name = data["name"]
            arguments = data["arguments"]
            handler = Hub(Handler)
            if handler.is_yield_function(name):
                for item in handler.register(name).generate(arguments):
                    response = json.dumps(item)
                    socket.send(bytes(response, encoding="utf-8"))
            else:
                response = handler.register(name).run(arguments)
                response = json.dumps(response)
                socket.sendall(bytes(response, encoding="utf-8"))
        except Exception as error:
            raise error
            view.red(error)

class Gui:
    def run(self):
        HOST, PORT = "localhost", 9998
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            server.serve_forever()