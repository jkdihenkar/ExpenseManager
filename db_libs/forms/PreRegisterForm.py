from flask_wtf import Form
from wtforms import *

class PreRegisterForm(Form):
    email_of_user = StringField("Enter your email : ")
    generate_otp = SubmitField("Generate OTP")