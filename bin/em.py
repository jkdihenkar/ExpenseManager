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
        em.py expense <from> <to> <amount> [<comment>]
        em.py listallusers
        em.py allexpenseto <uname>
        em.py allexpensefrom <uname>
        em.py allexpense <uname>
        em.py summary <uname>
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
            to_u = args[3]
            amt = float(args[4])
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
            em.py expense <from> <to> <amount>
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