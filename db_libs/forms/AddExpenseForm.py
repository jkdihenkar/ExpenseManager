from flask_wtf import Form
from wtforms import *
import sys
sys.path.append('../')

import connection

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AddExpenseForm(Form):

    conn = connection.connection()
    allresult = conn.getallusers()
    allusers = []
    for record in allresult:
        ob = (record[1], record[1])
        allusers.append(ob)

    FromMultipleList = MultiCheckboxField("From Expense : ", choices=allusers)
    confirm = PasswordField("Confirm : ")
    otp = PasswordField("OTP : ")
    submit = SubmitField("Register")
    ToSingleSelect = SelectField("To Expense : ", choices=allusers)
    ExpenseType = SelectField("Type : ", choices=[('SPLIT','SPLIT'),('GROUP','GROUP')])
    AmountInput = FloatField("Amount : ")
    CommentInput = TextAreaField("Comment : ")
    submit = SubmitField("Add Expense")