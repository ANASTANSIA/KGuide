from flask import Blueprint

user_management_blueprint = Blueprint('user_management', __name__, template_folder='templates')
from app.user_management import routes