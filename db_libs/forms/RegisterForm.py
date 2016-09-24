from flask_wtf import Form
from wtforms import *

class RegisterForm(Form):
    password = PasswordField("Password : ")
    confirm = PasswordField("Confirm : ")
    otp = PasswordField("OTP : ")
    submit = SubmitField("Register")