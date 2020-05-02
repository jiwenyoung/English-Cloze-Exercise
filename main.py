import argparse
import sys
from configuration.configuration import Configuration
from source.Fresh import Fresh
from database.Setup import Setup
from exercise.Exercise import Exercise
from database.Setup import Setup
from words.Words import Words

class View:
    def red(self, text):
        print(f"\033[1;31m{text}\033[0m")
        return self

class Bootstrap:
    def __init__(self):
        self.arguments = object()
        self.view = view
        self.config = Configuration()

    def parse_argv(self):
        """ parse cli arguments into list """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "navigation",
            nargs="?",
            help=self.config.literal["subcommand_help"],
            default="exam"
        )
        args = parser.parse_args()
        self.arguments = args
        return self

    def fresh(self):
        """ refetch data into database """
        fresh = Fresh()
        fresh.run()

    def setup(self):
        """ rebuild database structure """
        setup = Setup()
        setup.run()

    def exercise(self):
        """ roll out random questions to exercise """
        exercise = Exercise()
        exercise.run()

    def mistake(self):
        """ roll out mistaken questions to exercise """
        exercise = Exercise()
        exercise.run(1)

    def keywords(self):
        words = Words()
        words.run()

    def test(self):
        """ left for test new sub-command """
        pass

    def main(self):
        """ ENTRY """
        self.parse_argv()
        nav = self.arguments.navigation
        if nav == "fresh":
            self.fresh()
        elif nav == "setup":
            self.setup()
        elif nav == "exercise":
            self.exercise()
        elif nav == "mistake":
            self.mistake()
        elif nav == "keywords":    
            self.keywords()
        elif nav == "server":
            pass
        elif nav == "test":
            self.test()
        else:
            self.view.red(self.config.literal["unsupported_command"])
            sys.exit(1)

# start up the program
try:
    view = View()
    bootstrap = Bootstrap()
    bootstrap.main()
except Exception as error:
    raise error
    view.red(error)
