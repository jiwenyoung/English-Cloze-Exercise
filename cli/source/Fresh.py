import os,sys
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
from .Helper import Helper

class Fresh:
    def __init__(self):
        self.config = Configuration()
        self.count = 0
        self.status = ""
        self.helper = Helper()

    @View.log("Clear data existed in database...")
    def clearDB(self):
        with sqlite.connect(self.config.db_file) as connection:
            sqls = [
                "delete from questions",
                "delete from keywords"
            ]
            for sql in sqls:
                connection.execute(sql)
                connection.commit()
        return self

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
        url = self.config.source
        source = RssSource(url, self.keywords)
        if source.collect() != False:
            data = source.collect().fetch().save().output()
            with threading.Lock() as lock:
                self.count = self.count + len(data)
        return self

    @View.log("Start fresh questions from Medium...")
    def freshMedium(self):
        url = self.config.source
        source = MediumSource(url, self.keywords)
        if source.collect() != False:
            data = source.collect().fetch().save().output()
            with threading.Lock() as lock:
                self.count = self.count + len(data)
        return self

    def run(self, is_ask_user_input=0):
        self.status = self.helper.isConnected()
        if self.status == "NONETWORK":
            View.red("Network connection failure...")

        self.clearDB()

        is_ignore_default_keywords = False
        if is_ask_user_input == 0:
            #Decide if ignore keywords from network source
            is_ignore_default_keywords = input(
                self.config.literal["is_ignore_default_keywords"]
            )
            is_ignore_default_keywords = is_ignore_default_keywords.lower()
            if is_ignore_default_keywords == "":
                is_ignore_default_keywords = "n"
            if is_ignore_default_keywords == "n":
                is_ignore_default_keywords = False
            else:
                is_ignore_default_keywords = True
        elif is_ask_user_input == 1:
            is_ignore_default_keywords = True
        elif is_ask_user_input == 2:
            is_ignore_default_keywords = False

        #Get keywords list
        keywords = Keywords()
        if is_ignore_default_keywords == True:
            keywords.user_words().save()
        else:
            keywords.collect().fetch().parse().user_words().save()
        keywords = self.getKeywords()

        #Compose questions from all source
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
        if self.status != "NONETWORK":
            tasks.append(threading.Thread(target=rss_task))
            if self.status == "GLOBAL":
                tasks.append(threading.Thread(target=medium_task))
        
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

        View.green(
            self.config.literal["fresh_questions_total"].format(self.count))

    def test(self):
        """ left for test new model """
        pass
