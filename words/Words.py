import sys
from .Codec import Codec
from .View import View
from configuration.configuration import Configuration

class Words:
    def __init__(self):
        self.codec = Codec()
        self.config = Configuration()
        self.view = View()

    def push(self, word):
        with open(self.config.keyword_user_file, 'a+b') as file:
            file.write(word)
        return self

    def pull(self):
        words = set()
        with open(self.config.keyword_user_file, 'r+b') as file:
            while True:
                word = file.read(32)
                if not word:
                    break
                word = Codec().decode(word)
                if word != None:
                    words.add(word)
        return words

    def compose(self, words):
        binary = b''
        for word in words:
            binary_word = self.codec.encode(word)
            binary = binary + binary_word
        return binary

    def sync(self, binary):
        with open(self.config.keyword_user_file, "wb") as file:
            file.write(binary)
        return self

    def search(self,keyword):
        words = self.pull()
        find = [ item for item in words if item == keyword ]
        if len(find) > 0:
            self.view.white(self.config.literal["search_user_keyword_found"].format(keyword))
        else:
            self.view.red(self.config.literal["search_user_keyword_unfound"])
        return self

    def remove(self, word):
        words = self.pull()
        words = set(item for item in words if item != word)
        binary = self.compose(words)
        self.sync(binary)
        self.view.white(self.config.literal["remove_user_keyword"].format(word))
        return self

    def display(self):
        words = self.pull()
        self.view.display_words(words)
        return self

    def run(self):
        def is_has_comma(args):
            comma = False
            for arg in args:
                if ',' in arg:
                    comma = True
            return comma        

        def compose_muilt_args(args):
            arg_str = ""
            for arg in args:
                arg_str = arg_str + f" {arg}"
            arguments = set(arg_str.split(","))
            return arguments

        def compose_single_arg(args):
            word = ""   
            if len(args) > 1:
                word = " ".join(args).strip()
            else:
                word = args[0]
            return word

        while True:
            keyword = self.view.green_input("KEYWORDS")
            parse = keyword.split(" ")
            command = parse[0].lower()
            if len(parse) >= 2:
                args = parse[1:]

                words = []
                if is_has_comma(args):
                    words = compose_muilt_args(args)
                else:
                    words.append(compose_single_arg(args))

                if command == "add":
                    for word in words:
                        word = self.codec.encode(word)
                        self.push(word)                                

                elif command == "remove":
                    self.remove(word)
                
                elif command == "search":
                    self.search(word)
                
                else:
                    self.view.red(self.config.literal["unsupported_command"])
            else:
                if command == "exit" or command == "quit":
                    break
                elif command == "list":
                    self.display()
                else:
                    self.view.red(self.config.literal["unsupported_command"])
