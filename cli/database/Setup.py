import sys
import os
import sqlite3 as sqlite
from configuration.configuration import Configuration
from .View import View


class Setup:
    def __init__(self):
        self.config = Configuration()

    @View.log(text="Cleaning existed tables...")
    def clean(self):
        with sqlite.connect(self.config.db_file) as connection:
            cursor = connection.cursor()

            # Check if tables exists in database
            # if exists , drop it
            show_table_sql = "select name from sqlite_master where type='table';"
            tables = cursor.execute(show_table_sql)
            tables = tables.fetchall()
            if len(tables) > 0:
                is_drop_tables = input("Do you want to drop tables?(Y/N)")
                is_drop_tables = is_drop_tables.lower()
                if is_drop_tables == "y" or is_drop_tables == "yes":
                    drop_table_sqls = []
                    drop_table_sqls.append("drop table questions")
                    drop_table_sqls.append("drop table keywords")
                    for index, sql in enumerate(drop_table_sqls):
                        connection.execute(sql)
                        connection.commit()
                        View.progress(len(drop_table_sqls), index)
                    print("\n", end="\n")
                else:
                    sys.exit(0)
        return self

    @View.log(text="Create new database structure...")
    def create(self):
        with sqlite.connect(self.config.db_file) as connection:
            # Create Table
            sqls = []

            # question table
            # sentence
            # keyword  the correct answer
            # chocies  the four options
            # status 0 = untouched 1 = error
            sqls.append("""CREATE TABLE questions (
                sentence TEXT NOT NULL,
                keyword  TEXT NOT NULL,
                choices  TEXT NOT NULL,
                status   INT  NOT NULL DEFAULT 0 
            )""")

            # keywords table
            sqls.append("""CREATE TABLE keywords (
                keyword  TEXT NOT NULL
            )""")

            for index, sql in enumerate(sqls):
                connection.execute(sql)
                View.progress(len(sqls), index)
            print("\n", end="\n")

            connection.commit()
            return self

    def run(self):
        self.clean().create()
