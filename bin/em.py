import sys

sys.path.append('../db_libs')
sys.path.append('../models')

import connection

help = \
    """
    Welcome to expense manager app by TheInnovators Community!

    usage:
        em.py [COMMAND] [ARGS-TO-COMMAND]
    examples:
        em.py adduser <username> <email-id>
        em.py expense <from> <amount> <to> [<comment>]
        em.py listallusers
        em.py allexpenseto <uname>
        em.py allexpensefrom <uname>
        em.py allexpense <uname>
        em.py summary <uname>
        em.py split <cs users> <amount> <to> [<cmt>]
        em.py group <cs users> <amount> <to> [<cmt>]
        em.py mailsummary <uname>
    """

class em():
    def __init__(self):
        self.con = connection.connection()
        self.con.init_tables()

    def adduser(self, args):
        if not len(args) == 4:
            print(help)
        else:
            print("Adding user {}".format(args[2]))
            em.con.add_user(args[2], args[3])
            em.con.cleanup()

    def addexpense(self, args):
        if not len(args) >= 5:
            print(help)
        else:
            from_u = args[2]
            to_u = args[4]
            amt = float(args[3])
            if len(args) > 5:
                cmt = args[5]
            else:
                cmt = ''
            print("Adding expense {} to {} : {}".format(from_u, to_u, amt))
            em.con.add_expense(from_u, to_u, amt, cmt)
            em.con.cleanup()

    def list_all_users(self):
        res = em.con.getallusers()
        for row in res:
            print(row)
        em.con.cleanup()

    def generate_summary(self, uname):
        self.con.print_summary(uname)
        em.con.cleanup()

    def generate_mail_summary(self, uname):
        self.con.mail_summary(uname)
        em.con.cleanup()

    def split_add(self, csv_users, to_user, amount, cmt=''):
        if csv_users == 'all':
            from_users = [ 'kishan', 'jigar', 'hardik', 'parakh', 'parth', 'jv', 'jd' ]
            from_users.remove(to_user)
        else:
            from_users = csv_users.split(',')
        self.split_add_internal_api(from_users,to_user,amount,cmt)
        self.con.cleanup()

    def split_add_internal_api(self,from_users, to_user, amount, cmt=''):
        u_amount = amount / (len(from_users) + 1)
        for u in from_users:
            self.con.add_expense(u, to_user, u_amount, cmt)
        self.con.con.commit()

    def group_add(self, csv_users, to_user, amount, cmt=''):
        if csv_users == 'all':
            from_users = [ 'kishan', 'jigar', 'hardik', 'parakh', 'parth', 'jv', 'jd' ]
            from_users.remove(to_user)
        else:
            from_users = csv_users.split(',')
        self.group_add_internal_api(from_users, to_user, amount, cmt)
        self.con.cleanup()


    def group_add_internal_api(self, from_users, to_user, amount, cmt=''):
        for u in from_users:
            self.con.add_expense(u, to_user, amount, cmt)
        self.con.con.commit()

if __name__=='__main__':
    em = em()
    if len(sys.argv) < 2:
        print(help)

    else:
        args = sys.argv
        command = args[1]

        if command == 'adduser':
            """
            em.py adduser <username> <email-id>
            """
            em.adduser(sys.argv)

        elif command == 'expense':
            """
            em.py expense <from> <amount> <to>
            """
            em.addexpense(sys.argv)

        elif command == 'listallusers':
            """
            em.py listallusers
            """
            em.list_all_users()

        elif command == 'allexpenseto':
            """
            em.py allexpenseto <uname>
            """
            res = em.con.getallexpense(args[2], 'to')
            for row in res:
                print(row)

        elif command == 'allexpensefrom':
            """
            em.py allexpensefrom <uname>
            """
            res = em.con.getallexpense(args[2], 'from')
            for row in res:
                print(row)

        elif command == 'allexpense':
            """
            em.py allexpense <uname>
            """
            res = em.con.getallexpense(args[2])
            for row in res:
                print(row)

        elif command == 'summary':
            """
            em.py summary <uname>
            """
            em.generate_summary(args[2])

        elif command == 'split':
            """
            #python3.5 em.py split jd,jv,kishan 80 parth cmt
            """
            if len(args)>5:
                cmt = ' '.join(args[5:])
            else:
                cmt = ''
            em.split_add(args[2], args[4], float(args[3]), cmt)

        elif command == 'group':
            """
            em.py group jd,jv,kishan 20 parth [<cmt>]
            """
            if len(args) > 5:
                cmt = ' '.join(args[5:])
            else:
                cmt = ''
            em.group_add(args[2], args[4], float(args[3]), cmt)

        elif command=="mailsummary":
            """
            em.py mailsummary <uname>
            """
            em.generate_mail_summary(args[2])
