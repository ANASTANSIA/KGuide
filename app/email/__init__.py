from flask import Blueprint

email_blueprint = Blueprint('email', __name__,template_folder="templates")


from app.email import email,forms