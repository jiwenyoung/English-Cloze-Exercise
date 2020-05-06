class OutputLog:
    def __init__(self):
        self.log = []

    def write(self,line):
        if line != '\n':
            line = line.replace("\033[1;32m","")
            line = line.replace("\033[0m","")
            self.log.append({ "line" : line})

    def flush(self):
        self.log = []