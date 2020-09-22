from app import app, db,login
from flask import render_template,redirect,current_app
from flask import flash, url_for
from flask_login import login_user, logout_user, current_user
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import Role, User

from urllib import request
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse
from _datetime import datetime
from app.auth import auth_blueprint
from app.auth.email import send_password_reset_email
from app.auth.forms import ResetPasswordForm, ResetPasswordRequestForm

# @app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template ('index.html')
#    # return 'Welcome home'

@auth_blueprint.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect (url_for('user_management.index'))  

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.check_password.data):
            flash ('Invalid Username or password')
            return redirect(url_for('authentication.login'))
        #admin login
        # if user is 'admin100' and user.check_password(form.check_password.data):
        #     flash ('Welcome to admin section!!')
        #     return redirect(url_for('AdminProgramManagement.index'))
            

        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('user_management.index')
            flash ('Login success!')
        return redirect(next_page)
        
        return redirect(next_page or url_for('user_management.index'))
    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_management.index'))

@auth_blueprint.route('/register_admin')
def register_admin():
      if not User.query.filter(User.username=='admin100').first():
            
            user1 = User(username='admin100', email='admin100@gmail.com')
            user1.set_password('adminpassword12345')
            user1.roles.append(Role(name='Admin'))
            db.session.add(user1)
            db.session.commit()
        
    

@auth_blueprint.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_management.index'))

    form = RegistrationForm()

    if form.validate_on_submit():
      
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        #user.roles.append(Role(name='App_main_user'))
        db.session.add(user)
        db.session.commit()

        flash('Regisration Successful!!')
        return redirect(url_for('authentication.login'))

    return render_template('auth/register.html', form=form)

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('user_management.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your for information to Reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password.html',form=form)
    

def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    
    if not user:
        return redirect(url_for('index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
            
        user.setPassword(form.password.data)
        db.session.comit()
        
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
