import os

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

basedir = os.path.abspath(os.path.dirname(__file__))


# class that stores configuration variables
class Config(object):
    # configuration settings defined as class variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'just-crack-it-you-stupid-fool'
    # secret key value is sometimes used as a cryptographic key  ,usefull yo generate tokenns or signatures
    # used by web forms to  protect web forms against cross site request forgery

    # Sqlite database using sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'chickenApp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get("MAIL_PORT") or 35)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['anastansiaserem55@gmail.com']
    APP_ADMIN = 'anastansiaserem@gmail.com'
    ##sendgrid api
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    
    
    
    
    
    #flask-User settings
    USER_APP_NAME = "Chicken App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

    
    UPLOAD_FOLDER ='app/static/uploads'
    ALLOWED_EXTENSIONS = set(['pdf','png','jpg','jpeg'])
  
    # max post per page
    POSTS_PER_PAGE = 25
   

    BOOTSTRAP_SERVE_LOCAL = True
    EXPLAIN_TEMPLATE_LOADING  = True
    ELASTICSEARCH_URL= os.environ.get('ELASTICSEARCH_URL')
    # ELASTICSEARCH_URL=http://localhost:9200
    
    
    #flask apscheduler
    JOBS = [
        {
        'id':'age',
        'func':'app.tasks:age_incrementer',
        'trigger': 'interval',
        'hours':1,
        'replace_existing':True
        }
    ]
    SCHEDULER_API_ENABLED = True
    
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(SQLALCHEMY_DATABASE_URI)
    }
    