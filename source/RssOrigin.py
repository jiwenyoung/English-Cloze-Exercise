import html
import random
import re
import xml.etree.cElementTree as ET
from urllib import request
from configuration.configuration import Configuration
from .Origin import Origin
from .Question import Question
from .Helper import Helper
from .View import View

class RssOrigin(Origin, Helper):
    def __init__(self, url):
        self.url = url
        self.doc = ""
        self.rawtext = ""
        self.data = set()
        self.config = Configuration()

    @View.log("Reading RSS feeds...")
    def pull(self):
        View.render(self.config.literal["pull_rss_prompt"].format(self.url))
        req = request.Request(self.url)
        req.add_header('User-Agent', self.config.useragent)
        with request.urlopen(req) as reponse:
            self.doc = reponse.read().decode("utf-8")
        return self

    @View.log("Parse raw data from rss url...")
    def parse(self):
        """ parse raw data from url to a long string of texts """
        tree = ET.fromstring(self.doc)
        rule = re.compile(r'<[^>]+>', re.S)
        result = ""
        for item in tree.iter("item"):
            for element in item:
                if "content" in element.tag:
                    chunk = rule.sub('', element.text)
                    chunk = html.unescape(chunk)
                    result = result + chunk
        self.rawtext = result
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
