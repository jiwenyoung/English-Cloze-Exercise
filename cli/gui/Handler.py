from exercise.Exercise import Exercise
from collections import deque
import time

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
        mylist = [{'a': "c"}, {'b': "e"}, {'c': 6}]
        for item in mylist:
            time.sleep(1)
            yield item
