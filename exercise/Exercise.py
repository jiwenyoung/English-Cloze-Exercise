import sys
import sqlite3 as sqlite
from .Quesiton import Question
from .View import View
from configuration.configuration import Configuration

class Exercise:
    def __init__(self):
        self.config = Configuration()
        self.done = set()
        self.question = object()
        self.view = View()
        self.score = {
            "correct": 0,
            "wrong": 0
        }

    def pull(self, status=0):
        with sqlite.connect(self.config.db_file) as connetion:
            cursor = connetion.cursor()
            sql = "select rowid,sentence,keyword,choices \
                   from questions where status=? \
                   order by random() limit 1"
            while True:
                question = cursor.execute(sql, (status,))
                question = question.fetchall()
                if len(question) == 0:
                    self.view.warning(self.config.literal["no_question"])
                    sys.exit(1)
                else:
                    question = question[0]

                id, sentence, keyword, choices = question
                if id not in self.done:
                    self.done.add(id)
                    self.question = Question(id, sentence, keyword, choices)
                    break
                else:
                    continue
        return self

    def interact(self):
        option_symbols = ["A", "B", "C", "D"]

        # display
        self.view.sentence(self.question.sentence, 80)
        self.view.options(option_symbols, self.question.choices)

        # choice dict is created
        options = dict()
        for symbol, choice in zip(option_symbols, self.question.choices):
            options[symbol] = choice

        # input and evauate
        while True:
            selected = input(self.config.literal["input"])

            # remove this question , unimplemented
            if selected.upper() == self.config.remove_question_key:
                self.question.correct_remove()
                self.view.remove()
                break

            # quit the program
            if selected.upper() == self.config.quit_key:
                correct = self.score["correct"]
                wrong = self.score["wrong"]
                total = correct + wrong
                self.view.score(total, correct, wrong)
                sys.exit(0)

            if selected.upper() in option_symbols:
                selected = options[selected.upper()]
                if self.question.evaluate(selected):
                    self.question.correct_remove()
                    self.view.evaluate(True)
                    self.score["correct"] = self.score["correct"] + 1
                else:
                    self.question.wrong_update().wrong_log(selected)
                    for index, value in options.items():
                        if value == self.question.keyword:
                            self.view.evaluate(False, index)
                            break
                    self.score["wrong"] = self.score["wrong"] + 1
                break
            else:
                continue
        return self

    def run(self, status=0):
        try:
            if status not in [0, 1]:
                self.view.warning(self.config.literal["exception"])
                sys.exit(1)

            if status == 0:
                self.view.clear().header(80).title("QUESTIONS")
            elif status == 1:
                self.view.clear().header(80, "Mistakes").title("QUESTIONS")

            while True:
                if status == 0:
                    self.pull().interact()
                elif status == 1:
                    self.pull(status).interact()

        except KeyboardInterrupt:

            correct = self.score["correct"]
            wrong = self.score["wrong"]
            total = correct + wrong
            self.view.score(total, correct, wrong)

        except Exception as error:
            raise error
