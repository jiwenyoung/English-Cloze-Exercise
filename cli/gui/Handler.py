import sys
from exercise.Exercise import Exercise
from collections import deque
from source.Fresh import Fresh
from database.Setup import Setup
from .OutputLog import OutputLog

Storage = {
    "exercise" : Exercise(),
    "question" : deque([],1)
}

class Handler:
    def __init__(self):
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
            "score" : self.exercise.score
        }
        if question.evaluate(answer):
            response["evaluate"] = True
            response["score"]["correct"] += 1 
            question.correct_remove()
        else:
            response["evaluate"] = False
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
                "error" : str(error)
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
            return {
                "error" : str(error)
            }