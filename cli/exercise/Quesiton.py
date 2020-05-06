import sqlite3 as sqlite
from datetime import datetime
from configuration.configuration import Configuration

class Question:
    def __init__(self, id, sentence, keyword, choices):
        self.id = id
        self.sentence = sentence
        self.keyword = keyword
        self.choices = choices.split(",")
        self.config = Configuration()

    def evaluate(self, selected):
        """ right or wrong """
        if selected.lower() == self.keyword.lower():
            return True
        else:
            return False

    def correct_remove(self):
        """ if answer is correct, remove it from database """
        with sqlite.connect(self.config.db_file) as connection:
            cursor = connection.cursor()
            sql = "delete from questions where rowid=?"
            cursor.execute(sql, (self.id,))
            connection.commit()
        return self

    def wrong_update(self):
        """ if answer is wrong, change its status """
        status = 1
        with sqlite.connect(self.config.db_file) as connection:
            cursor = connection.cursor()
            sql = "update questions set status=? where rowid=?"
            cursor.execute(sql, (status, self.id))
            connection.commit()
        return self

    def wrong_log(self, selected):
        """ if answer is wrong, log it into text file """
        now = datetime.now().strftime("%d %b %Y %H:%M:%S")
        logs = self.config.literal["wrong_log"].split("|")
        logs[0] = logs[0].format(now)
        logs[1] = logs[1].format(self.sentence)
        logs[2] = logs[2].format(" , ".join(self.choices),
                                 selected,
                                 self.keyword)
        with open(self.config.wrong_log,"at",encoding="utf8") as file:
            for log in logs:
                file.write(log)
                file.write("\r\n")
            file.write("\r\n")
        return self
