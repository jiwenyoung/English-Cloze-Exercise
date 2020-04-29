import sys
import threading
import requests
import fnmatch
from bs4 import BeautifulSoup as HTMLParser
from configuration.configuration import Configuration
from .MediumOrigin import MediumOrigin
from ..Source import Source
from ..View import View
from ..Helper import Helper

class MediumSource(Source):
    def __init__(self,file,keywords):
        self.config = Configuration()
        self.keywords = keywords
        self.file = file
        self.urls = []
        self.data = []
        self.helper = Helper()

    def get_blogs_of_author(self,author):
        url = ""
        if author.startswith("@"):
            url = f"https://{self.config.medium_domain}/{author}"
        else:
            url = f"https://{self.config.medium_domain}/@{author}"
            author = f"@{author}".strip()

        hrefs = set()
        with requests.get(url) as response:
            text = response.text
            parser = HTMLParser(text,"html.parser")
            blog_list = parser.findAll("div", {"class" : [ "r","s","y" ]} )
            for blog in blog_list:
                links = blog.findAll("a")
                for link in links:
                    link = link["href"]
                    format_author = f"/{author}/"
                    format_author = format_author.replace("\n","")
                    if format_author in link and "?source=" in link:
                        link = link.split("?")[0]
                        hrefs.add(link)
                    else:
                        if "?source=" in link:
                            link = link.split("?")[0]
                            pattern = f"https://*.{self.config.medium_domain}/*".replace("\n","")
                            if fnmatch.fnmatch(link,pattern):
                                link_segmants = link.split("/")
                                if link_segmants[-1] != "":
                                    hrefs.add(link)

        urls = set()
        for href in hrefs:
            pattern = f"https://*.{self.config.medium_domain}/*".replace("\n","")
            if fnmatch.fnmatch(href,pattern):
                url = href
            else:    
                url = f"https://{self.config.medium_domain}{href}"
            urls.add(url)
        hrefs = urls
        return hrefs

    @View.log("Colleting URLs of Medium articles...")
    def collect(self):
        urls = []
        with open(self.file) as file:
            all_lines = self.helper.read_block(file,"medium")
            for item in all_lines:
                if item.startswith("#"):
                    continue
                elif "https:" in item and f"{self.config.medium_domain}/" in item:
                    segaments = item.split(f"{self.config.medium_domain}/")
                    if segaments[1] != "":
                        urls.append(item.strip())
                elif item.startswith("@"):
                    hrefs = self.get_blogs_of_author(item)
                    for href in hrefs:
                        urls.append(href)
                else:
                    continue
        self.urls = list(set(urls))
        if len(self.urls) == 0:
            return False
        else:
            return self

    @View.log("Getting data from Medium...")
    def fetch(self):
        def gain(url):
            try:
                origin = MediumOrigin(url)
                data = origin.pull().parse().clean().filter(self.keywords).output()
                with threading.Lock():
                    for question in data:
                        self.data.append(question)
            except Exception as error:
                View.red(error)                

        tasks = []
        for url in self.urls:
            tasks.append(threading.Thread(target=gain,args=(url,)))
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

        return self

    @View.log("Save questions from Medium into database...")
    def save(self):
        for question in self.data:
            question.save()
        return self

    def output(self):
        return self.data


