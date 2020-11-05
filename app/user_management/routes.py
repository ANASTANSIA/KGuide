from app import app, db,login
from flask import render_template,redirect,g
from flask import flash, url_for
from flask_login import login_user, logout_user, current_user,login_required
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import Event, Permission, Program, Stage, User

from urllib import request
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse
from _datetime import datetime
from app.user_management import user_management_blueprint
from sqlalchemy.orm import session
from app.products.forms import SearchForm

@user_management_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    # g.locale = str(get_locale())
        
@user_management_blueprint.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@user_management_blueprint.route('/')
@user_management_blueprint.route('/index')
def index():
   
    return render_template ('user_management/index.html')
   # return 'Welcome home'



    
@user_management_blueprint.route('/specific_program/<program_id>', methods = ['GET','POST'])
@login_required
def specific_program(program_id):
    
    program = Program.query.filter(Program.program_id == program_id).first()
    print (program)
    results = db.session.query(Stage.stage_name,Stage.start,Stage.end,Event.event_description).join(Event).join(Program).\
        filter(Program.program_id == program_id).all()
    
    result_dict = {}    
    result =convert(results,result_dict)

    return render_template('user_management/specific_program.html', result=result,program = program)

def convert(tupl, dic):
    y=()
    x = []
    for name,start,end,event in tupl:
        x.append(name)
        x.append(start)
        x.append(end)
        s=x[-3:]
        y=tuple(s)
        dic.setdefault(y,[]).append(event)
        
        
    return dic


@user_management_blueprint.route('/get_program', methods=['GET','POST'])
@login_required
def get_program():
    programs = Program.query.all()
    return render_template('user_management/programs.html',programs=programs)





@user_management_blueprint.route('/feeds')
def feeds():
    return 'I am feeds'

@user_management_blueprint.route('/vaccines')
def vaccines():
    return 'I am Vaccines'


@user_management_blueprint.route('/market')
def market():
    return 'I am Market'

@user_management_blueprint.route('/housing')
def housing():
    return 'I am Housing'