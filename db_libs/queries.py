import sys

import connection

class queries():
    def __init__(self):
        self.init_all_queries()

    def init_all_queries(self):
        self.member_table = \
            """
            CREATE TABLE members(
               id INTEGER PRIMARY KEY     AUTOINCREMENT,
               name           TEXT,
               email          TEXT
            );
            """

        self.expense_table = \
            """
            CREATE TABLE expenses(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               from_member  TEXT,
               to_member  TEXT,
               amount REAL,
               comment TEXT,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """

        self.check_table_in_db = \
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='{}';
            """

        self.add_user = \
            """
            INSERT INTO members (name, email) VALUES ('{name}','{email}')
            """