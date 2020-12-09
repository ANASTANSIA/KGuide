from flask_mail import Message
from app import mail
from app.models import User
from flask import render_template,request,redirect,url_for
from app import current_app
from threading import Thread
from flask.helpers import flash
from flask_login.login_manager import current_user


def send_async_email(app, msg):
    with current_app.app_context():
        mail.send(msg)

def send_mail(subject,sender,recipients, text_body,html_body):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html= html_body
    Thread(target=send_async_email,args=(current_app,msg)).start()
    
    
    
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[Chicken APP] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html',user=user, token=token)
               )
    
    
def send_inquiry(user):
    
    recipient = current_app.config['DEFAULT_SENDER']
    user = User.query.filter(current_user.id).first()
    sender = user.email
    if request.method == "POST":
        body = request.form.get('message_body')    
        msg = Message('Chicken App Inquirries',sender=sender, recipients=[recipient])
        msg.body = (body)
        msg.html=('<p> {{ body }} </p> ')
        
        mail.send(msg)
        flash('Message Sent !!')
    
    return redirect(url_for('user_management.index'))