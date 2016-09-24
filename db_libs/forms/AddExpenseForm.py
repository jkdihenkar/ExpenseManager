from flask_wtf import Form
from wtforms import *
import sys
sys.path.append('../')

import connection


class AddExpenseForm(Form):
    def __init__(self):
        self.conn = connection.connection()
        self.allusers = self.conn.getallusers()
        self.FromMultipleList = SelectMultipleField("From Expense : ", choices=self.allusers)

    confirm = PasswordField("Confirm : ")
    otp = PasswordField("OTP : ")
    submit = SubmitField("Register")