from flask import Blueprint

admin_program_management_blueprint = Blueprint('program', __name__)


from app.auth import routes, forms