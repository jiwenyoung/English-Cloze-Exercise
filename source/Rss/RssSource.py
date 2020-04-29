import sys
import threading
from .RssOrigin import RssOrigin
from ..Source import Source
from ..View import View
from ..Helper import Helper

class RssSource(Source, Helper):
    def __init__(self, url, keywords):
        self.keywords = keywords
        self.url = url
        self.urls = []
        self.data = []

    @View.log("Colleting URLs of RSS feeds...")
    def collect(self):
        urls = []
        with open(self.url) as file:
            all_lines = super().read_block(file, "rss")
            for url in all_lines:
                if not url.startswith("#"):
                    urls.append(url.strip())
        self.urls = list(set(urls))
        if len(self.urls) == 0:
            return False
        else:
            return self

    @View.log("Getting data from RSS feeds...")
    def fetch(self):
        def gain(url):
            try:
                origin = RssOrigin(url)
                data = origin.pull().parse().clean().filter(self.keywords).output()
                with threading.Lock():
                    for question in data:
                        self.data.append(question)
            except Exception as error:
                View.red(error)

        tasks = []
        for url in self.urls:
            tasks.append(threading.Thread(target=gain, args=(url,)))
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

        return self

    @View.log("Save questions from RSS into database...")
    def save(self):
        for question in self.data:
            question.save()
        return self

    def output(self):
        return self.data

