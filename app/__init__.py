from flask import Flask
from flask import Flask, app, current_app, request
#from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
#from flask_babel import Babel, lazy_gettext as _l
import os
from config import Config


# app = Flask(__name__)

# # app.config.from_object(Config) #reads it and applies it
# db = SQLAlchemy(app) #db object represents the database


#crates and initializes the log in extension
login= LoginManager()

#Flask-Login provides a very useful feature that forces users to log in before they can view certain pages of the application. If a user who is not logged in tries to view a protected page, Flask-Login will automatically redirect the user to the login form, and only redirect back to the page the user wanted to view after the login process is complete.
# #For this feature to be implemented, Flask-Login needs to know what is the view function that handles logins.
login.login_view = 'login'
#login.login_message = _l('please log in to access this page')
mail = Mail()

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate() # object represents migration engine



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
   
    # db.init_app(app)
    #migrate.init_app(app,db)
    from app import models
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    # moment.init_app(app)
    # babel.init_app(app)
   
   
    #blueprint registration
#errors blueprint
    from app.errors import blueprint as errors_blueprint
    app.register_blueprint(errors_blueprint)

    #authentication blueprint
    from app.auth import auth_blueprint as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    #user blueprint
    from app.user import user_blueprint as user_blueprint
    app.register_blueprint(user_blueprint)
    
    from app.AdminProgramManagement import admin_program_management_blueprint as admin_program_management_blueprint
    app.register_blueprint(admin_program_management_blueprint)
    
    
    #user_management_blueprint
    from app.user_management import user_management_blueprint as user_management_blueprint
    app.register_blueprint(user_management_blueprint)
    #from app import routes,models,errors 
   
    
    # if not app.debug:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             secure = None
    #             if app.config['MAIL_USE_TLS']:
    #                 secure = ()
    #             mail_handler = SMTPHandler(
    #                 mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #                 fromaddr='no-reply@' + app.config['MAIL_SEVER'],
    #                 toaddrs=app.config['ADMINS'],subject='Chicken Rearing Application Failure',
    #                 credentials=auth, secure=secure)
    #             mail_handler.setLevel(logging.ERROR)
    #             app.logger.addHandler(mail_handler)

    #         if not os.path.exists('logs'):
    #             os.mkdir('logs')
    #         file_handler = RotatingFileHandler('logs/chicken.log',maxBytes=10240,
    #                     backupCount=10)
    #         file_handler.setFormatter(logging.INFO)
    #         app.logger.addHandler(file_handler)

    #         app.logger.setLevel(logging.INFO)
    #         app.logger.info('Chicken  Application')
            
    return app




from app import models


            
