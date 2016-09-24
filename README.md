#ExpenseManager

A very simple and extensible Python based ExpenseManager Utility Tool. 

Works on Python2.7 and uses SQlite to store your expenses.

Working examples : 

**1. Show Usage**
```
jd@jaypc:~/em/bin$ ./exec 

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
```

Start using it.

**2. Mailing Expense Details**
```
line# 145 :         self.mail_sender('<mailidhere@gmail.com>',  #set you mail ID here
...
...
line# 154 :            smtpObj.login(sender, '<passwordhere>')  #set your password
```

Once you set your mail ID credentials and you set mail ID appropriately while adding new users, you'll be able to alert the end users via EMAILs as well.

## By TheInnovators Community
