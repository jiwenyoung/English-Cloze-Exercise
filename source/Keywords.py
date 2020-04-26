import threading
import json
import sqlite3 as sqlite
from urllib import request
from queue import Queue
from configuration.configuration import Configuration
from .View import View

class Keywords:
    def __init__(self):
        self.config = Configuration()
        self.urls = set()
        self.data = []
        self.execlude = set()

    @View.log("Collect URLs for fetching keywords...")
    def collect(self):
        with open(self.config.keyword_urls) as file:
            for line in file:
                self.urls.add(line.strip())
        return self

    @View.log("Fetching URL ...")
    def fetch(self):
        def gain(url):
            try:
                req = request.Request(url)
                req.add_header('User-Agent', self.config.useragent)
                with request.urlopen(req) as response:
                    data = response.read().decode("utf-8")
                    with threading.Lock():
                        self.data.append(json.loads(data))
                    View.render(f"Fetching {url}")
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

    @View.log("Extra keywords from source...")
    def parse(self):
        words = []
        exclude = self.config.keyword_exclude.split(",")
        self.execlude = exclude
        for block in self.data:
            for word in block:
                if word not in self.data and word not in exclude:
                    words.append(word.strip())
        self.data = words
        return self

    @View.log("Append user customized keywords into list...")
    def user_words(self):
        with open(self.config.keyword_user_file) as file:
             for word in file:
                 if word not in self.data and word not in self.execlude:
                     self.data.append(word)
                 else:
                     continue
        return self             

    @View.log("Save keywords into database...")
    def save(self):
        with sqlite.connect(self.config.db_file) as connection:
            sql = "insert into keywords values (?)"
            for word in self.data:
                connection.execute(sql,(word,))
                connection.commit()
        return self

    def output(self):
        return self.data
