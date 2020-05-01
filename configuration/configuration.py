from configparser import ConfigParser
import sys

class Configuration:
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini",encoding="utf-8")

        blocks = []
        with open("config.ini") as file:
            for line in file:
                if line.startswith("["):
                    block = line[1:-2]
                    if block != "literal":
                        blocks.append(block)

        for key in config:
            if key in blocks:
                for item in config[key]:
                    setattr(self, item, config[key][item])
            elif key in ["literal"]:
                literal = dict()
                for item in config[key]:
                    literal[item] = config[key][item]
                setattr(self, "literal", literal)
