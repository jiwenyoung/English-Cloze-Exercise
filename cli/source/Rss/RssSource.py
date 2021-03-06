import sys
import threading
from .RssOrigin import RssOrigin
from ..Source import Source
from ..View import View
from ..Helper import Helper

class RssSource(Source):
    def __init__(self, url, keywords):
        self.keywords = keywords
        self.url = url
        self.urls = []
        self.data = []
        self.status = ""
        self.helper = Helper()

    @View.log("Colleting URLs of RSS feeds...")
    def collect(self):
        urls = []
        self.status = self.helper.isConnected()
        with open(self.url, encoding="utf-8") as file:
            all_lines = set()
            if self.status == "GLOBAL":
                all_lines = self.helper.read_block(file, "global-rss")
            elif self.status == "CHINA":
                all_lines = self.helper.read_block(file,"china-rss")
            else:
                View.red("Check your network connection...")
                sys.exit(1)

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
                View.red(url)
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

