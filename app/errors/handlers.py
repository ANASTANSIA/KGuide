from app import db
from flask import render_template
from app.errors import blueprint


@blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@blueprint.app_errorhandler
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'),500