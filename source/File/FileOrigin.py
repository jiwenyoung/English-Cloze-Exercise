from ..Origin import Origin
from ..Question import Question
from ..Helper import Helper
from ..View import View
from configuration.configuration import Configuration

class FileOrigin(Origin):
    def __init__(self, file):
        self.file = file
        self.doc = ""
        self.rawtext = ""
        self.data = set()
        self.config = Configuration()
        self.helper = Helper()

    @View.log("Reading file...")
    def pull(self):
        View.render(self.config.literal["pull_file_prompt"].format(self.file))
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
        sentences = self.helper.separate_text(rawtext)
        self.data = self.helper.clean_each_sentence(sentences,
                                                    self.config.sentence_shortest,
                                                    self.config.sentence_longest)
        return self

    @View.log("Transform data into questions...")
    def filter(self, keywords):
        data = []
        sentences = self.data
        filtered = self.helper.transform_sentenses_to_tuples(sentences, keywords)
        for element in filtered:
            sentence, keyword, choices = element
            data.append(Question(sentence, keyword, choices))
        self.data = data
        return self

    def output(self):
        return self.data
