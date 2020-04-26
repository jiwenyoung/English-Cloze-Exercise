import os
import threading
from .FileOrigin import FileOrigin
from .Source import Source
from .View import View

class FileSource(Source):
    def __init__(self,path,keywords):
        self.path = path
        self.keywords = keywords
        self.data = []
        self.files = []

    @View.log("Collect files available...")
    def collect(self):
        files = os.listdir(self.path)
        if len(files) == 0:
            return False
        else:
            self.files = files
            return self
    
    @View.log("Getting data from files...")
    def fetch(self):
        def gain(file):
            try:
                file = os.path.join(self.path,file)
                origin = FileOrigin(file)
                data = origin.pull().parse().clean().filter(self.keywords).output()
                with threading.Lock():
                    for question in data:
                        self.data.append(question)
            except Exception as error:
                View.red(error)

        tasks = []
        for file in self.files:
            tasks.append(threading.Thread(target=gain,args=(file,)))
        for task in tasks:
            task.start()
        for task in tasks:
            task.join()

        return self

    @View.log("Save questions from files into database...")
    def save(self):
        for question in self.data:
            question.save()
        return self

    def output(self):
        return self.data


