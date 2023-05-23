from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/')
def index():
    return redirect('/user/login')

@app.route('/user/login')
def login():
    if 'user_id' in session:
        return redirect('/dashboard')

    return render_template('index.html')

@app.route('/user/login/process', methods=['POST'])
def login_success():
    user = user.User.validate_login(request.form)
    if not user:
        return redirect('/user/login')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not user.User.validate_register(request.form):
        return redirect('/user/login')

    user_id = user.User.save_user(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/user/login')