
from flask_login import UserMixin, AnonymousUserMixin
from app import current_app,login,db

from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime
from hashlib import md5
from time import time
import jwt
from app.search import add_to_index,remove_from_index,query_index
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from lib2to3.pytree import Base
from sqlalchemy.types import Integer
from flask import json

#import jwt
class Permission:      
    COMMENT = 1    
    WRITE = 2    
    MODERATE = 4   
    ADMIN = 8
    
    
class SearchableMixin(object):
    
    @classmethod #associated with a class and not a particular instance
    #cls =====>method receives a class not an instance as its first argument
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__,expression,page,per_page)
        if total == 0:
            return cls.query.filter_by(id=0),0
        
        when = []
        
        for i in range(len(ids)):
            when.append((ids[i],i))
            
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)),total
        
        
    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add':list(session.new),
            'update': list(session.dirty),
            'delete':list(session.deleted)
        }
        
        
    @classmethod
    def after_commit(cls, session):
        
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
                
        for obj in session._changes['update']:
            if isinstance(obj,SearchableMixin):
                add_to_index(obj.__tablename__, obj)
                
        for obj in session._changes['delete']:
            if isinstance(obj,SearchableMixin):
                remove_from_index(obj.__tablename__,obj)
                
        session._changes = None
        
        
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__,obj)
            
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit',SearchableMixin.after_commit)
  


@login.user_loader
def load_user(id):
        return User.query.get(int(id))
    
subscription = db.Table('subscription',
                        # db.Column('subscription_id',db.Integer,primary_key=True),
                        db.Column('program', db.Integer, ForeignKey('program.program_id')),
                        db.Column('user', db.Integer, ForeignKey('user.id')),
                        db.Column('age',db.Integer)
                    )

class User(UserMixin,db.Model):
        id = db.Column(db.Integer,primary_key=True,nullable=False)
        username = db.Column(db.String(64),index=True,unique=True,nullable=False)
        email = db.Column(db.String(120), index=True,unique=True,nullable=False)
        password_hash = db.Column(db.String(128))
        

        about_me = db.Column(db.String(140))
        last_seen = db.Column(db.DateTime, default=datetime.utcnow)
        role_id = db.Column(db.Integer,db.ForeignKey('role.id',ondelete='CASCADE'))
        
        product = db.relationship('Product', backref='user', lazy='dynamic',cascade='all,delete,delete-orphan')
        
        subscriptions = db.relationship("Program",secondary=subscription, backref="subscribers")
        
        notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic',cascade='all,delete,delete-orphan') 
        
        

        def __repr__(self):
          
            
            return '<User {}>'.format(self.username)
       

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)


        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

        
        def avatar(self, size):
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size) 
            
            
        # Reset Password
        def get_reset_password_token(self,expires_in=1800):
            return jwt.encode(
                {'reset_password': self.id,'exp':time() + expires_in},
                  current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')  
            
        @staticmethod   #can be invoked directly from the class
        def verify_reset_password_token(token):
            try:
                id = jwt.decode(token, current_app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
            except:
                return
       
            return User.query.get(id)
      
       #user roles 
        def __init__(self, **kwargs):
            super(User, self).__init__(**kwargs)
            if self.role is None:
                if self.email == current_app.config['APP_ADMIN']:
                    self.role = Role.query.filter_by(name='Administrator').first()
                if self.role is None:
                    self.role = Role.query.filter_by(default=True).first()
       
        def can(self, perm):
                return self.role is not None and self.role.has_permission(perm)

        def is_administrator(self):
            return self.can(Permission.ADMIN)
        
        
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login.anonymous_user = AnonymousUser
        
        
            
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    # user_role = db.relationship('UserRoles', backref='role' )
    
   
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
            
            
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
     
    @staticmethod       
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT, Permission.WRITE],
            
            'Administrator': [Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
        
        
class Subscriptions(db.Model):
    user = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
    program =db.Column(db.Integer, db.ForeignKey('program.program_id'),primary_key=True, nullable=False)
    age = db.Column(db.Integer,nullable=False,index=True)
    subscription_day= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    
    # def increment_age(self,age):       
    #     age += 1
    #     Subscriptions.age = age
        
    #     db.session.commit()
        
    
    
            

class Product(SearchableMixin,db.Model):
    __searchable__ = ['product_type']
    product_id = db.Column(db.Integer,primary_key=True,nullable=False)
    product_type = db.Column(db.String(64),index=True,nullable=False)
    quantity = db.Column(db.Float,nullable=False)
    product_description = db.Column(db.String(200),nullable=False)
    image_path = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    comment = db.relationship('Comment' , backref='product',lazy='dynamic',cascade='all,delete,delete-orphan')
    
    def __repr__(self):
            return '<Product {}>'


class Program(SearchableMixin, db.Model):
    __searchable__= ['program_name']
    program_id = db.Column(db.Integer,primary_key=True)
    program_name = db.Column(db.String(64),index=True,nullable=False)
    program_description = db.Column(db.String(140),index=True,nullable=False)
    
    stages = db.relationship('Stage', backref='Program', lazy='dynamic' ,cascade='all,delete,delete-orphan')
    
    
    def __repr__(self):
        return '<Program {}>'.format(self.program_name)
    
class Stage(db.Model):
    __searchable__ = ['stage_name']
    stage_id = db.Column(db.Integer,primary_key=True)
    stage_name = db.Column(db.String,index=True,nullable=False)
    start = db.Column(db.Integer,index=True,nullable=False)
    end = db.Column(db.Integer,index=True,nullable=False)
    
    program_id = db.Column(db.Integer,db.ForeignKey('program.program_id'))
    events = db.relationship('Event', backref='stage', lazy='dynamic',cascade='all,delete,delete-orphan')

    
    def __repr__(self):
        return '<Stage {}>'.format(self.stage_name)
    
    
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_description = db.Column(db.String,index=True,nullable=False)
    
    stage_id = db.Column(db.Integer,db.ForeignKey('stage.stage_id'))
    
    
    
    def __repr__(self):
        return '<Event {}>'.format(self.event_description)
    
    
    
    
# class Subs(db.Model):
#     subscription_id = db.Column(db.Integer,primary_key=True)
#     age = db.Column(db.Integer,index=True,nullable=False)
#     program_id = db.Column(db.Integer, ForeignKey('program.program_id')),
#     user_id = db.Column(db.Integer, ForeignKey('user.id'))


# Comment to product post

class Comment(db.Model):
    _N = 6

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    path = db.Column(db.Text, index=True)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
   
    product_id = db.Column(db.Integer,db.ForeignKey('product.product_id'))
    
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')
    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id,self._N)
        db.session.commit()
        
        
    def level(self):
        return len(self.path)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(128), index=True)
    payload_json = db.Column(db.Text)
    
    
    def get_data(self):
        return json.loads(str(self.payload_json))   

