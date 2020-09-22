import os

basedir = os.path.abspath(os.path.dirname(__file__))


# class that stores configuration variables
class Config(object):
    # configuration settings defined as class variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # secret key value is sometimes used as a cryptographic key  ,usefull yo generate tokenns or signatures
    # used by web forms to  protect web forms against cross site request forgery

    # Sqlite database using sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'chickenApp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 35)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['anastansiaserem55@gmail.com']
    UPLOAD_FOLDER ='app/static/uploads'
    ALLOWED_EXTENSIONS = set(['pdf','png','jpg','jpeg'])
  
    # max post per page
    POSTS_PER_PAGE = 25
   

    BOOTSTRAP_SERVE_LOCAL = True
    EXPLAIN_TEMPLATE_LOADING  = True
