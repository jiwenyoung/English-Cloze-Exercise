import sys
import sqlite3 as sqlite
from .Quesiton import Question
from .View import View
from configuration.configuration import Configuration

class Exercise:
    def __init__(self):
        self.config = Configuration()
        self.question = None
        self.view = View()
        self.score = {
            "correct": 0,
            "wrong": 0
        }

    def pull(self, status=0):
        with sqlite.connect(self.config.db_file) as connetion:
            cursor = connetion.cursor()

            sql = "select count(*) from questions where status=?" 
            total = cursor.execute(sql,(status,))
            total = total.fetchone()
            total = total[0]

            sql = "select rowid,sentence,keyword,choices \
                   from questions where status=? \
                   order by random() limit 1"
            question = cursor.execute(sql, (status,))
            question = question.fetchone()
            if question == None:
                self.question = None
            else:
                id, sentence, keyword, choices = question
                self.question = Question(id, sentence, keyword, choices)
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

            # remove this question
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
                self.pull(status)
                if self.question != None:
                    self.interact()
                else:
                    self.view.warning(self.config.literal["no_question"])
                    sys.exit(1)

        except KeyboardInterrupt:

            correct = self.score["correct"]
            wrong = self.score["wrong"]
            total = correct + wrong
            self.view.score(total, correct, wrong)

        except Exception as error:
            raise error

    def output(self):
        if self.question != None:
            return self.question
        else:
            return False
