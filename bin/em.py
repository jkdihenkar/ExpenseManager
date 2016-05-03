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
    """

class em():
    def __init__(self):
        self.con = connection.connection()
        self.con.init_tables()


if __name__=='__main__':
    em = em()
    if len(sys.argv) < 2:
        print(help)

    else:
        args = sys.argv
        command = args[1]

        if command == 'adduser':
            if not len(sys.argv)==4:
                print(help)
            else:
                print("Adding user {}".format(args[2]))
                em.con.add_user(args[2], args[3])
                em.con.cleanup()