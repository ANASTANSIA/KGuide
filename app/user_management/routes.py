from app import app, db,login
from flask import render_template,redirect
from flask import flash, url_for
from flask_login import login_user, logout_user, current_user
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import Event, Program, Stage, User

from urllib import request
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse
from _datetime import datetime
from app.user_management import user_management_blueprint
from sqlalchemy.orm import session

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()

@user_management_blueprint.route('/')
@user_management_blueprint.route('/index')
def index():
    return render_template ('user_management/index.html')
   # return 'Welcome home'


def view_programs():
    programs = Program.query.all()
    programArray = []
    for program in programs:
        programObj={}
        programObj['program_id'] = program.program_id
        programObj['programe_name'] = program.programe_name
        programObj['program_description'] = program.program_description
        programArray.append(programObj)
        
        return render_template('programs.html', programArray)
    
    

def specific_program(program_id):
    #results = session.query(Stage, Event).filter(Stage.stage_id == Event.stage_id).all()
    result = session.query(Stage).join(Event).filter(Event.stage_id == Stage.stage_id,program_id=Program.program_id)
    stageList=[]
    for stage in result:
       for event in stage.events:
           stageObj={}
           stageObj['stage_id'] = stage.stage_id
           stageObj['stage_name'] = stage.stage_name
           stageObj['start'] = stage.start
           stageObj['end'] = stage.end
           
           eventObj={}
           eventObj['event_id'] = event.event_id
           eventObj['event_description'] = event.event_description
           
           stageObj['event'] = eventObj
           
           stageList.append(stageObj)
    
    return render_template('program.html',stageList)
           
           
           
   
    # stages = Stage.query.filter_by(program_id=program_id)
    # stageArray = []
    # for stage in stages:
    #     stageObj={}
    #     stageObj['stage_id'] = stage.stage_id
    #     stageObj['stage_name'] = stage.stage_name
    #     stageObj['start'] = stage.start
    #     stageObj['end'] = stage.end
        
    #    #events = Event.query.filter_by(Event.stage_id=Stage.stage_id).all()
    #     eventList =[]
    #     for event in events:
    #         eventObj ={}
    #         eventObj['event_id'] = event.event_id
    #         eventObj['event_description'] = event.event_description
    #         eventList.append(eventObj)
    #     stageObj['event'] = stage.eventList
        
    #     stageArray.append(stageObj)
            
        
            
        
    
    
    # return render_template('view_program.html',stageArray)
    
    

@user_management_blueprint.route('/feeds')
def feeds():
    return 'I am feeds'

@user_management_blueprint.route('/vaccines')
def vaccines():
    return 'I am Vaccines'


@user_management_blueprint.route('/market')
def market():
    return 'I am Market'

@user_management_blueprint.route('/get_program', methods=['GET'])
def get_program():
    program = Program.query.all()
    return render_template('user_management/programs.html')
