from .Origin import Origin
from .Question import Question
from .Helper import Helper
from .View import View

class FileOrigin(Origin, Helper):
    def __init__(self, file):
        self.file = file
        self.doc = ""
        self.rawtext = ""
        self.data = set()

    @View.log("Reading file...")
    def pull(self):
        View.render(f"Reading {self.file}")
        doc = ""
        with open(self.file) as file:
            for line in file:
                doc = doc + line
        self.doc = doc
        return self

    @View.log("Parse raw file data...")
    def parse(self):
        self.rawtext = self.doc
        return self

    @View.log("Clean extra chars...")
    def clean(self):
        rawtext = self.rawtext
        sentences = super().separate_text(rawtext)
        self.data = super().clean_each_sentence(sentences, 10, 20)
        return self

    @View.log("Transform data into questions...")
    def filter(self, keywords):
        data = []
        sentences = self.data
        filtered = super().transform_sentenses_to_tuples(sentences, keywords)
        for element in filtered:
            sentence, keyword, choices = element
            data.append(Question(sentence, keyword, choices))
        self.data = data
        return self

    def output(self):
        return self.data
