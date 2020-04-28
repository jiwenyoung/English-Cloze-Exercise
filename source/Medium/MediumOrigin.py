import html
import random
import re
import requests 
from bs4 import BeautifulSoup as HTMLParser
from configuration.configuration import Configuration
from ..Origin import Origin
from ..Question import Question
from ..Helper import Helper
from ..View import View

class MediumOrigin(Origin, Helper):
    def __init__(self, url):
        self.url = url
        self.doc = ""
        self.rawtext = ""
        self.data = set()
        self.config = Configuration()

    @View.log("Reading Medium article...")
    def pull(self):
        View.render(self.config.literal["pull_medium_prompt"].format(self.url))
        with requests.get(self.url) as reponse:
            self.doc = reponse.text
        return self

    @View.log("Parse raw data from rss url...")
    def parse(self):
        """ parse raw data from url to a long string of texts """
        parser = HTMLParser(self.doc,"html.parser")
        paragraphs = ""
        article = ""
        if len(parser.findAll("article")) > 0: 
            article = parser.findAll("article")[0]
            article = article.findAll("p")
            for paragraph in article:
                paragraphs = paragraphs + paragraph.text
            self.rawtext = paragraphs
        return self

    @View.log("Clean extra chars...")
    def clean(self):
        """ clean extra chars in string and save data into set """
        rawtext = self.rawtext
        sentences = super().separate_text(rawtext)
        data = super().clean_each_sentence(sentences,
                                           self.config.sentence_shortest,
                                           self.config.sentence_longest)
        self.data = data
        return self

    @View.log("Transform data into questions...")
    def filter(self, keywords):
        """ transform data from sentence list to list of Question Object """
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
