

from app import db
from werkzeug import redirect
from flask.helpers import url_for
from app.models import Event, Program, Stage
from app.AdminProgramManagement.forms import ProgramForm, StageForm
from app.AdminProgramManagement import admin_program_management_blueprint
from flask.json import jsonify
from flask.templating import render_template
from urllib import request


@admin_program_management_blueprint.route('/index')
@login_required
def index():
    
    return render_template('AdminProgramManagement/index.html')


@admin_program_management_blueprint.route('/add_program')
@login_required
def add_program():
    form = ProgramForm()
    
    if form.validateonsubmit():
        program=Program(programe_name=form.program_name.data, program_description=form.program_description.data)
        
        db.session.add(program)
        db.session.commit()
    return redirect(url_for('/view_program'))


@admin_program_management_blueprint.route('/add_stage<program>', method=['GET', 'POST'])
@login_required
def add_stage(program):
    
    form = StageForm()
    if request.method == 'POST':
          data = request.get_json()
          data = data.parse(data)
    
          for key in data:
              stage_name = data.stage_name
              start = data.start
              end=data.end
              
              event_description = 
             
            ##get the data from the form
            stage = Stage(stage_name=form.stage_name.data,start=form.start.data,end=form.end.data)
            if stage:
                db.add(stage)
                db.commit(stage)
                
                event = Event(event = form.event_description.data)
                
                db.add(stage)
                db.commit(stage)
            
        
        
  
        
    return redirect(url_for('/view_program', form=form)
        
# @admin_program_management_blueprint.route('/add_event<stage>')
# def add_event(stage):
#     form = StageForm()
#     events = []
#     for event in events:
#         event = Event(event_description=form.event_description.data)
        
#         db.session.add(event)
#         db.session.commit()
    
    
#     return render_template('')        
        
        
@admin_program_management_blueprint.route('/stage/<program>')       

def select_stage(program):
    stages = Stage.query.filter_by(program=program).all()
    
    stageArray = []
    for stage in stages:
        stageObj={}
        stageObj['stage_id'] = stage.stage_id
        stageObj['name'] = stage.stage_name
        stageArray.append(stageObj)
        
    #return jsonify('stages':stageArray)
    return render_template('AdminProgramManagement.program.html')

        
        
        