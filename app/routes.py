from app import app, db,login
from flask import render_template,redirect
from flask import flash, url_for
from flask_login import login_user, logout_user, current_user
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import User

from urllib import request
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse
from _datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template ('index.html')
   # return 'Welcome home'

@app.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:
        return redirect (url_for('index'))  

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.check_password.data):
            flash ('Invalid Username or password')
            return redirect(url_for('login'))

        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
            flash ('Login success!')
        return redirect(next_page)
        
        return redirect(next_page or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Regisration Successful!!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


    # user profile //details
@app.route('/user/<username>')
#@login_required   
def user(username):
    user = User.query.filter_by(username=username).first_or_404()


    return render_template('user.html',user=user)


@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your profile has been updated!')
        return redirect(url_for('edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html',form=form)




@app.route('/feeds')
def feeds():
    return 'I am feeds'

@app.route('/vaccines')
def vaccines():
    return 'I am Vaccines'


@app.route('/market')
def market():
    return render_template('vet.html')