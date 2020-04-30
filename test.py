import json
import random
import copy
from pprint import pprint

def choice(keywords, keyword):
    def compare(keywords, keyword, i):
        data = []
        for word in keywords:
            if i < len(word) and i < len(keyword):
                if keyword[i] == word[i]:
                    data.append(word)
        return data

    i = 0
    choices = []
    original = copy.deepcopy(keywords)
    while True:
        keywords = compare(keywords, keyword, i)
        i = i + 1
        if len(keywords) <= 4:
            if keyword not in keywords:
                keywords.append(keyword)
            if len(keywords) <= 4:    
                difference_count = 4 - len(keywords)
                difference = list(set(original).difference(set(keywords)))
                addition = random.sample(difference,difference_count)
                choices.append([*keywords,*addition])
            else:
                choices.append(keywords)
            break
        else:
            choices.append(keywords)

    choices = choices[-1]
    choices.remove(keyword)
    choices = random.sample(choices, 3)
    choices.append(keyword)
    choices = list(set(choices))
    random.shuffle(choices)
    return choices


def main():
    with open("prepositions.json") as file:
        data = file.read()
        data = json.loads(data)
        data = ["turn|off","turn|on","turn|in","in","on","off"]
        for i in range(100):
            choices = choice(data, "turn|on")
            print(len(choices))


main()
