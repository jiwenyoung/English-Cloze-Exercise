from configparser import ConfigParser

class Configuration:
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini")

        for key in config:
            if key in ["files", "keys", "domain", "sentence"]:
                for item in config[key]:
                    setattr(self, item, config[key][item])
            elif key in ["literal"]:
                literal = dict()
                for item in config[key]:
                    literal[item] = config[key][item]
                setattr(self, "literal", literal)
