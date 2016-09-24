from flask_wtf import Form
from wtforms import *

class LoginForm(Form):
    email = TextField("Username : ")
    password = PasswordField("Password : ")
    submit = SubmitField("Login")