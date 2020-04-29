import os
import asyncio
import sqlite3 as sqlite
import threading
from configuration.configuration import Configuration
from .Rss.RssOrigin import RssOrigin
from .Rss.RssSource import RssSource
from .File.FileOrigin import FileOrigin
from .File.FileSource import FileSource
from .Medium.MediumOrigin import MediumOrigin
from .Medium.MediumSource import MediumSource
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

    @View.log("Start fresh questions from Medium...")
    def freshMedium(self):
        url = self.config.medium_urls
        source = MediumSource(url, self.keywords)
        if source.collect() != False:
            data = source.collect().fetch().save().output()
            with threading.Lock() as lock:
                self.count = self.count + len(data)
        return self

    def run(self):
        is_ignore_default_keywords = input(
            self.config.literal["is_ignore_default_keywords"])
        is_ignore_default_keywords = is_ignore_default_keywords.lower()
        if is_ignore_default_keywords == "":
            is_ignore_default_keywords = "n"

        keywords = Keywords()
        if is_ignore_default_keywords == 'y':
            keywords.user_words().save()
        else:
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

        def medium_task():
            try:
                self.setKeyword(keywords).freshMedium()
            except:
                View.red(error)

        tasks = []
        tasks.append(threading.Thread(target=file_task))
        tasks.append(threading.Thread(target=rss_task))
        tasks.append(threading.Thread(target=medium_task))
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

        View.green(
            self.config.literal["fresh_questions_total"].format(self.count))

    def test(self):
        pass
