import sys
import os

sys.path.append('../db_libs')

import connection

def test_db_create_table():
    con_details = {
        'dbpath': '.',
        'dbname': 'test.db'
    }
    con_utils = connection.connection(**con_details)

    qstring = \
    """
    CREATE TABLE testtable(
       ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL
    );
    """

    result = con_utils.exec_query(qstring)

def test_check_testtable_exist():
    con_details = {
        'dbpath': '.',
        'dbname': 'test.db'
    }
    con_utils = connection.connection(**con_details)

    res = con_utils.check_if_table_exist('testtable')

    return res

if __name__=='__main__':
    #test_db_create_table()
    print(test_check_testtable_exist())