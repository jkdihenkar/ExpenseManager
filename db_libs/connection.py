import os
APP_PATH,SCRIPT_NAME = os.path.split(os.path.realpath(__file__))

import sys
sys.path.append(os.path.join(APP_PATH, '../bin'))
sys.path.append(os.path.join(APP_PATH, APP_PATH))

import sqlite3
import math
import smtplib
import queries
from password_script import password

DB_PATH = os.path.join(APP_PATH, '../db')

class connection():
    def __init__(self, dbname='master.db', dbpath=DB_PATH):
        self.db_dir = dbpath
        self.master_db = os.path.join(self.db_dir, dbname)
        #print(self.master_db)
        self.con = sqlite3.connect(self.master_db,check_same_thread=False)
        self.q = queries.queries()


    def check_if_table_exist(self, table_name):
        qstring = self.q.check_table_in_db.format(table_name)
        res = self.exec_query(qstring)
        return len(res.fetchall()) > 0

    def check_user_exist(self, uname):
        q = self.q.check_user_exist.format(name=uname)
        res = self.exec_query(q)
        return  len(res.fetchall())>0

    def init_tables(self):
        if not self.check_if_table_exist('members'):
            self.exec_query(self.q.member_table)
        if not self.check_if_table_exist('expenses'):
            self.exec_query(self.q.expense_table)

    def add_user(self, name, email):
        if not self.check_user_exist(name):
            q = self.q.add_user.format(name=name, email=email)
            print("Executing : {}".format(q))
            self.exec_query(q)
        else:
            print("User : {} already exist, select a different name!".format(name))

    def add_expense(self, from_u, to_u, amt,cmt=''):
        if not self.check_user_exist(from_u):
            print("User '{}' doesnot exist!")
            return False
        if not self.check_user_exist(to_u):
            print("User '{}' doesnot exist!")
            return False
        q = self.q.add_expense.format(from_u, to_u, amt, cmt)
        self.exec_query(q)

    def getallusers(self):
        q = self.q.getallusers
        res = self.exec_query(q)
        return res.fetchall()


    def exec_query(self, qstring):
        return self.con.execute(qstring)

    def exec_script(self, qstring):
        return self.con.executescript(qstring)

    def getallexpense(self, uname, direc=''):
        if direc == 'to':
            q = self.q.getallexpense_to.format(name = uname)
            print(q)
        elif direc == 'from':
            q = self.q.getallexpense_from.format(name = uname)
            print(q)
        else:
            q = self.q.getallexpense.format(name = uname)
            print(q)

        res = self.exec_query(q)

        return res.fetchall()

    def getallexpense_fromto(self, funame, tuname):
        q = self.q.getallexpense_fromto.format(fname=funame,tname=tuname)
        # print(q)

        res = self.exec_query(q)

        return res.fetchall()

    def list_all_user_except(self, uname):
        q = self.q.getalluserexcept.format(name=uname)
        res = self.exec_query(q)
        return res.fetchall()

    def print_summary(self, uname):
        other_users = self.list_all_user_except(uname)
        for tup in other_users:
            u = tup[0]
            # print("About user = '{}'".format(u))

            # Amount init to 0 if to_user = u amt--
            # Amount from_user = u amt++
            amount = float(0)

            exps = self.getallexpense_fromto(uname, u)
            for exp in exps:
                a = float(exp[0])
                amount = float(amount - float(a))

            exps = self.getallexpense_fromto(u, uname)
            for exp in exps:
                a = float(exp[0])
                amount = float(amount + a)

            if amount>0:
                print("Member {} has to give you {} Rs".format(u,math.ceil(amount)))
            else:
                print("You have to give {} {} Rs".format(u,-math.ceil(amount)))

    def getmailid(self, uname):
        q = self.q.getmailid.format(name=uname)
        res = self.exec_query(q)
        return res.fetchall()

    def mail_summary(self, uname):
        other_users = self.list_all_user_except(uname)
        emailid = self.getmailid(uname)
        email = emailid[0][0]
        summary_content = ''
        for tup in other_users:
            u = tup[0]
            # print("About user = '{}'".format(u))

            # Amount init to 0 if to_user = u amt--
            # Amount from_user = u amt++
            amount = 0.00

            exps = self.getallexpense_fromto(uname, u)
            for exp in exps:
                a = float(exp[0])
                amount = float(amount - a)

            exps = self.getallexpense_fromto(u, uname)
            for exp in exps:
                a = float(exp[0])
                amount = float(amount + a)

            if amount > 0:
                print("Member {} has to give you {} Rs".format(u, math.ceil(amount)))
                summary_content = '\n'.join([summary_content,"Member {} has to give you {} Rs".format(u, math.ceil(amount))])
            else:
                print("You have to give {} {} Rs".format(u, -math.ceil(amount)))
                summary_content = '\n'.join([summary_content, "You have to give {} {} Rs".format(u, -math.ceil(amount))])
        self.mail_sender('jkdihenkar.projects@gmail.com',
                         email,
                         'Summary Sender Service | Expense Manager',
                         summary_content)

    def mail_sender(self, sender, recievers, subject_content, mail_content):
        try:
            smtpObj = smtplib.SMTP('smtp.gmail.com:587')
            smtpObj.starttls()
            smtpObj.login(sender, password)
            msg = "\r\n".join([
                "From: jkdihenkar.projects@gmail.com",
                "To: "+recievers,
                "Subject: "+subject_content,
                "",
                mail_content
            ])
            smtpObj.sendmail(sender, recievers, msg)
            print("Successfully sent email")
        except:
            print("Error: unable to send email")
            raise

    def cleanup(self):
        self.con.commit()
        self.con.close()

