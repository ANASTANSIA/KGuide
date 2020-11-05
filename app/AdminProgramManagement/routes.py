

from app import db

from flask import url_for,redirect,request
from app.models import Event, Program, Stage
# from app.AdminProgramManagement.forms import ProgramForm, StageForm
from app.AdminProgramManagement import admin_program_management_blueprint
from flask.json import jsonify
from flask.templating import render_template
from dns.resolver import query
from flask.helpers import flash, make_response
import json
from wtforms.csrf import session
from wtforms import form
from sqlalchemy  import update
from app.decorators import admin_required
from flask_login import current_user,login_required
from itertools import groupby
from operator import itemgetter


@admin_program_management_blueprint.route('/index',methods=['POST','GET'])
@login_required
@admin_required
def index():
    
    return ('This is index page')
    # return redirect(url_for('AdminProgramManagement.fetch_programs'))

@admin_program_management_blueprint.route('/add_program', methods=['POST','GET'])
@login_required
@admin_required
def add_program():
    
    if request.method == 'POST':
        request_result = request.form
        program_name = request_result.get('program_name')
        program_description = request_result.get('program_description')
        
        program = Program(program_name=program_name,program_description=program_description)
        db.session.add(program)
        db.session.commit()
        flash('Program Added!!')
    
    
    return redirect (url_for('AdminProgramManagement.fetch_programs'))
                     
                     
@admin_program_management_blueprint.route('/fetch_programs', methods=['POST','GET'])  
@login_required
@admin_required                  
def fetch_programs():
    programs = Program.query.all()
    
   
        
    return render_template('AdminProgramManagement/program.html',programs=programs)


@admin_program_management_blueprint.route('/program_update/<program_id>' ,methods = ['POST','GET'])
@login_required
@admin_required
def program_update(program_id):
    
    return render_template('AdminProgramManagement/update_program.html',program_id=program_id)


@admin_program_management_blueprint.route('/update_program/<program_id>' ,methods = ['POST','GET'])
@login_required
@admin_required
def update_program(program_id):
    
    program = Program.query.filter(Program.program_id == program_id).first()
    
    if request.method == 'POST':
        req = request.form
        program.program_name = req.get('program_name')
        program.program_description = req.get('program_description')
        
        # stmt = Program.update().where(Program.c.program_id == program_id).\
        #     values(program_name=program_name_update,program_description=program_description_update)
            
        db.session.commit()
        
        
    programs = Program.query.all()
    
   
        
    return render_template('AdminProgramManagement/program.html',programs=programs)
        
    # return redirect('AdminProgramManagement.fetch_programs')
       
        
        
@admin_program_management_blueprint.route('/delete_program/<program_id>' ,methods = ['POST','GET'])
@login_required
@admin_required
def delete_program(program_id):
    
    result = db.session.query(Program).get(program_id)
    db.session.delete(result)
    db.session.commit()
    
    return redirect(url_for('AdminProgramManagement.fetch_programs'))


# @admin_program_management_blueprint.route('/add_stage/<program_id>', methods = ['POST','GET'])
# @login_required
# @admin_required
# def add_stage(program_id):
#     program_id=program_id
    
#     return render_template('AdminProgramManagement/add_stage.html',program_id=program_id)
    
    


@admin_program_management_blueprint.route('/add_stage/<program_id>' ,methods = ['POST','GET'])
@login_required
@admin_required
def add_stage(program_id):

    if request.method == 'POST' and program_id is not None:
            
            stage_name = request.form['stage_name']
            start = request.form['start']
            end = request.form['end']
            event_list = request.form.getlist("TableData")  ###NOT WORKING
            # event_list = json.loads(events)
            
            print(stage_name)
            print(event_list)
           
            stage = Stage(stage_name=stage_name,start=start,end=end,program_id = program_id)
            for event_input in range(len(event_list)):
                stage.event.append(event_input)
            
            db.session.add(stage)
            db.session.commit()
            print('Submission Sucessful')
            
            res = make_response(jsonify(event_list,stage_name,start,end), 200)

            # return res
            return redirect (url_for('AdminProgramManagement.view_program', program_id = program_id))

       
            
    else:
        return render_template('AdminProgramManagement/add_stage.html',program_id=program_id)
    
    return redirect (url_for('AdminProgramManagement.view_program', program_id = program_id))
    




@admin_program_management_blueprint.route('/view_program/<program_id>', methods=['POST','GET'])  
@login_required
@admin_required
def view_program(program_id):
    program = Program.query.filter(Program.program_id == program_id).first()
    

    results = db.session.query(Stage.stage_name,Stage.start,Stage.end,Event.event_description).join(Event).join(Program).\
        filter(Program.program_id == program_id).all()

     
    print(results) 
    print(program)
    result_dict = {}
    result =convert(results,result_dict)
    # list_result = [(k,v) for k,v in result.items()]
   
    return render_template('AdminProgramManagement/view_program.html',program_id = program_id,program=program,result=result)

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

@admin_program_management_blueprint.route('/delete_stage/<stage_id>', methods=['POST','GET'])
@login_required
@admin_required
def delete_stage(stage_id):
    
    result = db.session.query(Stage).get(stage_id)
    db.session.delete(result)
    db.session.commit()
    
    return redirect(url_for('AdminProgramManagement.view_program'))
        

@admin_program_management_blueprint.route('/update_stage/<stage_id>')   
@login_required
@admin_required     
def update_stage(stage_id):
     stage = Stage.query.filter(Stage.stage_id == stage_id).first()
     events = db.session.query(Event).join(Stage).filter(Stage.stage_id == stage_id).all()
    
     if request.method == 'POST':
         
         req = request.form
         stage.stage_name = req.get('stage_name')
         stage.start = req.get('start')
         stage.end = req.get('end')
         
         event_list=req.getlist('event_list')
         
         
         
         db.session.commit()
        
     return redirect(url_for('AdminProgramManagement.view_program'))
    
        
    
        
    

         
