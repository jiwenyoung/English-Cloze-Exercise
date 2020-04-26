import os,asyncio
import sqlite3 as sqlite
import threading
from configuration.configuration import Configuration
from .RssOrigin import RssOrigin
from .RssSource import RssSource
from .FileOrigin import FileOrigin
from .FileSource import FileSource
from .Keywords import Keywords
from .View import View

class Fresh:
    def __init__(self):
        self.config = Configuration()
        self.count = 0

    def setKeyword(self, keywords):
        self.keywords = keywords
        return self

    @View.log("Get keywords from database...")
    def getKeywords(self):
        keywords = []
        with sqlite.connect(self.config.db_file) as connection:
            cursor = connection.cursor()
            sql = "select keyword from keywords"
            data = cursor.execute(sql)
            for item in data:
                item = item[0].strip()
                keywords.append(item)
        keywords = list(set(keywords))
        return keywords

    @View.log("Start fresh questions from local files...")
    def freshFile(self):
        path = self.config.essay_path
        source = FileSource(path, self.keywords)
        if source.collect() != False:
            data = source.collect().fetch().save().output()
            with threading.Lock() as lock:
                self.count = self.count + len(data)
        return self

    @View.log("Start fresh questions from rss feeds...")
    def freshRss(self):
        url = self.config.rss_urls
        source = RssSource(url, self.keywords)
        if source.collect() != False:
            data = source.collect().fetch().save().output()
            with threading.Lock() as lock:
                self.count = self.count + len(data)
        return self

    def run(self):
        keywords = Keywords()
        keywords.collect().fetch().parse().user_words().save()

        keywords = self.getKeywords()
        def file_task():
            try:
                self.setKeyword(keywords).freshFile()
            except Exception as error:
                View.red(error)
        
        def rss_task():
            try:
                self.setKeyword(keywords).freshRss()
            except Exception as error:
                View.red(error)
        
        tasks = []
        tasks.append(threading.Thread(target=file_task))
        tasks.append(threading.Thread(target=rss_task))
        for task in tasks:
            task.start()
        for task  in tasks:
            task.join()

        View.green(self.config.literal["fresh_questions_total"].format(self.count))