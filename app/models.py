from app import db
from flask_login import UserMixin
from app import login,app,current_app,create_app

from werkzeug.security import generate_password_hash

from datetime import datetime
from hashlib import md5
from time import time
#import jwt




@login.user_loader
def load_user(user_id):
        return User.get(int(user_id))


class User(UserMixin,db.Model):
        user_id = db.Column(db.Integer,primary_key=True)
        username = db.Column(db.String(64),index=True,unique=True)
        email = db.Column(db.String(120), index=True,unique=True)
        password_hash = db.Column(db.String(128))
        

        about_me = db.Column(db.String(140))
        last_seen = db.Column(db.DateTime, default=datetime.utcnow)
        
        product = db.relationship('Product', backref='author', lazy='dynamic')

        def __repr__(self):
                return '<User {}>'.format(self.username)
       

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)


        def check_password(self, password):
            return check_password(self.password_hash, password)

        
        def avatar(self, size):
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size) 
            
            
        # # Reset Password
        # def get_Reset_password_token(self,expires_in=600):
        #     return jwt.encode(
        #         {'reset_password': self.id,'exp':time() + expires_in},
        #           app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')  
            
            
        # def verify_reset_password_token(token):
        #     try:
        #         id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        #     except:
        #         return
        #     return User.query.get(user_id)
        
        
            
class Role(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id',ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id',ondelete='CASCADE'))
    
class Product(db.Model):
    product_id = db.Column(db.Integer,primary_key=True)
    product_type = db.Column(db.String(64),index=True)
    quantity = db.Column(db.Float)
    product_description = db.Column(db.String(200))
    image_path = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
    def __repr__(self):
            return '<Product {}>'.format(self.body)


class Program(db.Model):
    program_id = db.Column(db.Integer,primary_key=True)
    program_name = db.Column(db.String(64),index=True)
    program_description = db.Column(db.String(140),index=True)
    
    stage = db.relationship('Stage', backref='stage', lazy='dynamic')
    
    
    def __repr__(self):
        return '<Program {}>'.format(self.body)
    
class Stage(db.Model):
    stage_id = db.Column(db.Integer,primary_key=True)
    stage_name = db.Column(db.String,index=True)
    start = db.Column(db.Integer,index=True)
    end = db.Column(db.Integer,index=True)
    
    program_id = db.Column(db.Integer,db.ForeignKey('program.program_id'))
    events = db.Column('Event')

    
    def __repr__(self):
        return '<Stage {}>'.format(self.body)
    
    
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_description = db.Column(db.String,index=True)
    
    stage_id = db.Column(db.Integer,db.ForeignKey('stage.stage_id'))
    
    def __repr__(self):
        return '<Event {}>'.format(self.body)