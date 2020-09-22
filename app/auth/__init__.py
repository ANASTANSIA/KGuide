from flask import Blueprint

auth_blueprint = Blueprint('authentication', __name__,template_folder="templates")


from app.auth import email,routes,forms