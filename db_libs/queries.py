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

        self.check_user_exist = \
            """
            SELECT * from members WHERE name='{name}'
            """

        self.check_email_exist = \
            """
            SELECT * from members WHERE email='{email}'
            """

        self.add_expense = \
            """
            INSERT INTO expenses (from_member, to_member, amount, comment) VALUES ('{}','{}',{},'{}')
            """

        self.getallusers = \
            """
            SELECT * FROM members
            """

        self.getallexpense_to = \
            """
            SELECT * from expenses where to_member='{name}'
            """

        self.getallexpense_from = \
            """
            SELECT * from expenses where from_member='{name}'
            """

        self.getallexpense = \
            """
            SELECT * from expenses where to_member='{name}' or from_member='{name}'
            """

        self.getalluserexcept = \
            """
            SELECT name from members where name!='{name}'
            """

        self.getallexpense_fromto = \
            """
            SELECT (amount) from expenses where from_member='{fname}' and to_member='{tname}'
            """

        self.getmailid = \
            """
            SELECT email from members where name='{name}'
            """

        self.update_user_password = \
            """
            UPDATE members_login SET password = '{hashed_password}' WHERE email = '{email}';
            INSERT INTO members_login(email, password) SELECT '{email}', '{hashed_password}' WHERE changes() = 0;
            """

        self.validate_login = \
            """
            select * from members_login where email = '{email}' and password='{hashed_password}'
            """

        self.get_password_for_email = \
            """
            select password from members_login where email = '{email}'
            """