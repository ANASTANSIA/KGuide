from flask import Blueprint

admin_program_management_blueprint = Blueprint('AdminProgramManagement', __name__,template_folder="templates")


from app.AdminProgramManagement import routes,reports