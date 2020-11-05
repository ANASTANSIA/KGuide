from flask import Blueprint

product_blueprint = Blueprint('products',__name__,template_folder="templates")
from app.products import forms,routes
