import sys
import sqlite3 as sqlite
from exercise.Exercise import Exercise
from collections import deque
from source.Fresh import Fresh
from words.Words import Words
from words.Codec import Codec
from database.Setup import Setup
from .OutputLog import OutputLog
from configuration.configuration import Configuration

Storage = {
    "exercise" : Exercise(),
    "question" : deque([],1)
}

class Handler:
    def __init__(self):
        self.config = Configuration()
        self.exercise = Storage["exercise"]
        self.question = Storage["question"]

    def rollout(self):
        question = self.exercise.pull().output()
        self.question.append(question)
        data = {
            "id": question.id,
            "sentence": question.sentence,
            "keyword": question.keyword,
            "choices": question.choices
        }
        return data

    def evaulate(self,answer):
        question = self.question.pop()
        response = {
            "evaluate" : False,
            "info" : "",
            "score" : self.exercise.score
        }
        if question.evaluate(answer):
            response["evaluate"] = True
            response["info"] = self.config.literal["right"]
            response["score"]["correct"] += 1 
            question.correct_remove()
        else:
            response["evaluate"] = False
            response["info"] = self.config.literal["wrong"].format(question.keyword)
            response["score"]["wrong"] += 1
            question.wrong_update().wrong_log(answer)
        return response

    def fresh(self):
        try:
            fresh = Fresh()
            log = OutputLog()
            console = sys.stdout
            sys.stdout = log
            fresh.run(2)
            sys.stdout = console
            summary = log.log[-1]
            return summary
        except Exception as error:
            return {
                "line" : str(error)
            }

    def setup(self):
        try:
            dbsetup = Setup()
            log = OutputLog()
            console = sys.stdout
            sys.stdout = log
            dbsetup.run()
            sys.stdout = console
            return log.log[-1]
        except Exception as error:
            raise error
            return {
                "line" : str(error)
            }

    def remove(self):
        try:
            question = self.question.pop()
            question.correct_remove()
            return {
                "done" : True
            }
        except Exception as error:
            return {
                "done" : False,
                "error" : str(error)
            }

    def total(self):
        try:
            with sqlite.connect(self.config.db_file) as connection:
                cursor = connection.cursor()
                sql = "select count(*) from questions"
                rows = cursor.execute(sql)
                rows = rows.fetchall()
                return {
                    "done" : True,
                    "total" : rows[0][0]
                }
        except Exception as error:
            return {
                "done" : False,
                "error" : str(error)
            }

    def get_source_list(self):
        try:
            lines = []
            with open(self.config.source) as file:
                for line in file:
                    lines.append(line.strip())
            return lines
        except Exception as error:
            return [ str(error) ]

    def save_source_list(self, text):
        try:
            with open(self.config.source,'wt') as file:
                 file.write(text)
            return {
                "info" : "source list has been updated"
            }
        except Exception as error:
            return {
                "info" : str(error)
            }

    def get_config(self):
        try:
            lines = []
            with open(self.config.config) as file:
                for line in file:
                    lines.append(line.strip())
            return lines
        except Exception as error:
            return [ str(error) ]

    def save_config(self,text):
        try:
            with open(self.config.config,"wt") as file:
                file.write(text)
            return {
                "info" : "config file has been modified"
            }
        except Exception as error:
            return {
                "info" : str(error)
            }

    def get_keywords(self):
        try:
            words = Words()
            return list(words.pull())
        except Exception as error:
            return [ str(error) ]

    def save_keywords(self,text):
        try:
            words = Words()
            wordlist = text.split(",")
            wordlist = [ word.strip() for word in wordlist ]
            wordlist = [ word for word in wordlist if word != "" ]
            wordlist = list(set(wordlist))
            binary = words.compose(wordlist)
            words.sync(binary)
            return {
                "info" : "Key words list has been modified"
            }
        except Exception as error:
            return {
                "info" : str(error)
            }

    def get_wrong_log(self):
        try:
            with open(self.config.wrong_log) as file:
                for line in file:
                    yield { "line" : line }
        except Exception as error:
            return {
                "line" : str(error)
            }