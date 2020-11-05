
from flask import render_template,redirect,current_app

from flask import flash, url_for,request
from flask_login import login_user, logout_user, current_user

from werkzeug.exceptions import abort
from werkzeug.urls import url_parse
from _datetime import datetime
from app import  db
from app.auth import auth_blueprint
from app.email import email_blueprint
from app.forms import EditProfileForm, LoginForm, RegistrationForm
# from app.models import Role, User

from app.email.email import send_password_reset_email
from app.auth.forms import ResetPasswordForm, ResetPasswordRequestForm
from app.models import User
from flask_login import current_user,login_required


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
    if current_user.is_authenticated and  current_user.can:
        return redirect(url_for('user_management.index'))
    
    elif current_user.is_authenticated and current_user.is_administrator:
        return redirect(url_for('AdminProgramManagement.index'))
    
    else:
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            
            
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('authentication.login'))
            
            elif user.username == 'Administrator' and user.check_password and user.is_administrator:
                login_user(user,remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('AdminProgramManagement.index')
                    
            else: 
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('user_management.index')
                    
                return redirect(next_page)
            
        return render_template('auth/login.html', form=form)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user_management.index'))

# @auth_blueprint.route('/register_admin')
# def register_admin():
#       if not User.query.filter(User.username=='admin100').first():
            
#             user1 = User(username='admin100', email='admin100@gmail.com')
#             user1.set_password('adminpassword12345')
#             user1.roles.append(Role(name='Admin'))
#             db.session.add(user1)
#             db.session.commit()
        
    

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


@auth_blueprint.route('/reset_password_request', methods=['GET','POST'])

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('user_management.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your for information to Reset your password')
        return redirect(url_for('authentication.login'))
    return render_template('auth/reset_password_request.html',form=form)

    
@auth_blueprint.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('user_management.index'))
    user = User.verify_reset_password_token(token)
    
    if not user:
        return redirect(url_for('user_management.index'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
            
        user.set_password(form.password.data)
        db.session.comit()
        
        flash('Your password has been reset.')
        return redirect(url_for('authentication.login'))
    return render_template('email/reset_password.html', form=form)
