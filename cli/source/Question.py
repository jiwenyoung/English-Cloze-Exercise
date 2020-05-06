import sqlite3 as sqlite
from configuration.configuration import Configuration

class Question:
    """ MODEL """
    def __init__(self, sentence, keyword, choices):
        self.sentence = sentence
        self.keyword = keyword
        self.choices = choices

    def save(self):
        config = Configuration()
        with sqlite.connect(config.db_file) as connection:
            cursor = connection.cursor()

            # get data ready to insert
            sentence = self.sentence
            keyword = self.keyword
            choices = ",".join(self.choices)

            # search for current sentence in database
            search_sql = "select rowid from questions where sentence=?"
            cursor.execute(search_sql, (sentence,))
            connection.commit()
            search_result = cursor.fetchall()

            # if current sentence doesn't exist in database, insert it
            if len(search_result) == 0:
                sql = f"insert into questions values (?,?,?,0)"
                connection.execute(sql, (sentence, keyword, choices))
                connection.commit()
