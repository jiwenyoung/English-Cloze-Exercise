import threading
import json
import sqlite3 as sqlite
import requests
from queue import Queue
from configuration.configuration import Configuration
from .View import View
from .Helper import Helper
from words.Words import Words

class Keywords(Helper):
    def __init__(self):
        self.config = Configuration()
        self.urls = set()
        self.data = []
        self.execlude = set()

    @View.log("Collect URLs for fetching keywords...")
    def collect(self):
        with open(self.config.source, encoding="utf-8") as file:
            self.urls = super().read_block(file,"keywords")
        return self

    @View.log("Fetching URL ...")
    def fetch(self):
        def gain(url):
            try:
                with requests.get(url) as response:
                    data = response.text
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
        words = Words()
        word_list = words.pull()
        for word in word_list:
            if word not in self.data and word not in self.execlude:
                self.data.append(word)
            else:
                continue
        return self

    @View.log("Save keywords into database...")
    def save(self):
        with sqlite.connect(self.config.db_file) as connection:
            sql = "delete from keywords"
            connection.execute(sql)
            connection.commit()

            sql = "insert into keywords values (?)"
            for word in self.data:
                connection.execute(sql, (word,))
                connection.commit()
        return self

    def output(self):
        return self.data
