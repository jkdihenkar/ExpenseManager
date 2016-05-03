import sqlite3
import os
import queries

class connection():
    def __init__(self, dbname='master.db', dbpath='../db'):
        self.db_dir = dbpath
        self.master_db = os.path.join(self.db_dir, dbname)
        self.con = sqlite3.connect(self.master_db)
        self.q = queries.queries()


    def check_if_table_exist(self, table_name):
        qstring = self.q.check_table_in_db.format(table_name)
        res = self.exec_query(qstring)
        return len(res.fetchall()) > 0

    def init_tables(self):
        if not self.check_if_table_exist('members'):
            self.exec_query(self.q.member_table)
        if not self.check_if_table_exist('expenses'):
            self.exec_query(self.q.expense_table)

    def add_user(self, name, email):
        q = self.q.add_user.format(name=name, email=email)
        print("Executing : {}".format(q))
        self.exec_query(q)

    def exec_query(self, qstring):
        return self.con.execute(qstring)

    def cleanup(self):
        self.con.commit()
        self.con.close()

