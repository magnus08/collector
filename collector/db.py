import sqlite3

from collector.config import config


def get_db():
    print("+++ onfig {}".format(config))
    return sqlite3.connect(config['database'])
