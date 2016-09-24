from flask import Flask, render_template, request, redirect, make_response
from forms import LoginForm, RegisterForm, PreRegisterForm, AddExpenseForm
from utils import ExpenseManagerUtils
import hashlib
import connection


app = Flask(__name__)
app.secret_key = "highlysecret"
emutils = ExpenseManagerUtils.UtilsLib()
conn = connection.connection()

@app.route('/')
def reroute():
    return redirect('/login', code=302)

@app.route('/login')
def login():
    email = request.cookies.get('loggedin')
    if email and request.cookies.get('security_verify:'+email+':'+emutils.hash_of_hashpass(email)):
        return redirect('/home', code=302)
    else:
        form = LoginForm.LoginForm()
        return render_template('login.html', form=form)

@app.route('/register', methods = ['POST'])
def register():
    form = RegisterForm.RegisterForm()
    email = request.form['email_of_user']
    return render_template('register.html', form=form, email=email)

@app.route('/pre-register')
def pre_register():
    form = PreRegisterForm.PreRegisterForm()
    return render_template('pre-register.html', form=form)

@app.route('/validate-email',methods=['POST'])
def check_email_from_members():
    email = request.form['email_of_user']
    q = conn.q.check_email_exist.format(email=email)
    res = conn.exec_query(q)
    if len(res.fetchall()) > 0:
        return redirect('/otp-generate', code=307)
    else:
        return redirect('/login', code=302)
    pass

@app.route('/otp-generate', methods=['POST'])
def GenerateOTP():
    email = request.form['email_of_user']
    emutils.generate_otp_for_email(email)
    return redirect('/register', code=307)

@app.route('/validate-reset', methods=['POST'])
def validate_and_set_password():
    password = request.form['password']
    confirm_pass = request.form['confirm']
    email = request.form['email']
    otp = request.form['otp']
    if password==confirm_pass and emutils.validate_otp(email,otp):
        hashed_pass = hashlib.sha256(password.encode('utf-8'))
        hashed_password =hashed_pass.hexdigest()
        q = conn.q.update_user_password.format(email=email,hashed_password=hashed_password)
        emutils.clear_all_sessions(email)
        res = conn.exec_script(q)
        return redirect('/login', code=302)
    else:
        return redirect('/register', code=302)

@app.route('/validate-login', methods=['POST'])
def check_login():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    q = conn.q.validate_login.format(email=email,hashed_password=hashed_password)
    res = conn.exec_query(q)
    if len(res.fetchall()) > 0:
        emutils.set_session(email, request.remote_addr)
        resp_obj = make_response(redirect('/home', code=302))
        resp_obj.set_cookie('loggedin',email)
        resp_obj.set_cookie('security_verify:'+email+':'+emutils.hash_of_hashpass(email),'OK')
        return resp_obj
    else:
        return redirect('/login', code=302)

@app.route('/home')
def home():
    user = request.cookies.get('loggedin')
    if not emutils.check_and_update_exist_session(user):
        print("Fail check sessions")
        return render_template('login.html', form=LoginForm.LoginForm())
    elif request.cookies.get('security_verify:'+user+':'+emutils.hash_of_hashpass(user))!='OK':
        print("Fail security_Verify : {}".format('security_verify:'+emutils.hash_of_hashpass(user)))
        return render_template('login.html', form=LoginForm.LoginForm())

    form = AddExpenseForm.AddExpenseForm()
    return render_template('home.html',user=user,form=form)

if __name__ == "__main__":
    app.run(debug=True)
