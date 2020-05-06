import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from exercise.Exercise import Exercise
from configuration.configuration import Configuration

#Globale Variables
CONFIG = Configuration()
QUESTION = None
EXERCISE = Exercise()

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        exercise = Exercise()
        path = parse.urlparse(self.path).path
        query = parse.urlparse(self.path).query
        address, port = self.client_address

        def response(message):
            message = str(message)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(message.encode('utf-8'))

        def rollout():
            global QUESTION
            QUESTION = EXERCISE.pull().output()
            data = {
                "id": QUESTION.id,
                "sentence": QUESTION.sentence,
                "keyword": QUESTION.keyword,
                "choices": QUESTION.choices
            }
            response(data)

        def evaluate(answer):
            global QUESTION
            if QUESTION.evaluate(answer):
                correct(QUESTION)
                EXERCISE.score["correct"] = EXERCISE.score["correct"] + 1
                response({
                    "evaluate": "correct",
                    "score" : EXERCISE.score
                })
            else:
                wrong(QUESTION, answer)
                EXERCISE.score["wrong"] = EXERCISE.score["wrong"] + 1
                response({
                    "evaluate": "wrong",
                    "score" : EXERCISE.score    
                })
            QUESTION = None

        def correct(question):
            question.correct_remove()

        def wrong(question, answer):
            question.wrong_update().wrong_log(answer)

        if path == "/rollout":
            rollout()
        elif path == '/evaluate':
            answer = query.split("=")[1]
            evaluate(answer)
        else:
            response({"error": "invaild request"})

class Server:
    @staticmethod
    def run(server_class=HTTPServer, handler_class=GetHandler):
        port = int(CONFIG.server_port)
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f'Listening on port {port}')
        httpd.serve_forever()
