from app.user_management import user_management_blueprint
from app.models import Event, Program, Program, Stage, Subscriptions, User, subscription
from app import app, db,login
from flask import request,redirect,url_for
from flask_login import current_user,login_required

from sqlalchemy.orm import session
from flask.helpers import flash
from flask.templating import render_template


@user_management_blueprint.route('/subscribe/<program_id>' ,methods=['GET','POST'])
@login_required
def subscribe(program_id):
    
    # program = Program.query.filter(Program.program_id == program_id).first()
    # user = User.query.filter(User.id == current_user.id).first()
    if request.method == "POST":
        user=current_user.id
        program = program_id
        age = request.form.get('age')
        subscriptions = Subscriptions(user = user,program=program,age=age)
        
        db.session.add(subscriptions)
    
       
       
        db.session.commit()
        
       
        print('Success')
    
    return redirect(url_for('user_management.specific_program',program_id=program_id))



@user_management_blueprint.route('/subscribe_all' ,methods=['GET','POST'])
@login_required
def subscribe_all():
    programs = Program.query.all()
    user = current_user.id
    subss = Subscriptions.query.all()
  
        
    if request.method == "POST":
            
        age = request.form.get('age')
        for subs in subss:
            someone=subs.user
            theirprogram = subs.program
            
        for prog in programs:
            if someone == user  and theirprogram == prog.program_id:
                flash('already subscribed to this program')
                continue
        
            subscription = Subscriptions(user=user,program=prog.program_id,age=age)
            print('success!!!!!!')
            db.session.add(subscription)
            db.session.commit()
        
        
    return redirect(url_for('user_management.get_program'))

@user_management_blueprint.route('/get_user_programs/<user>' ,methods=['GET','POST'])
@login_required
def get_user_programs(user):
    us = user
    stmt_user = db.session.query(Subscriptions).join(User).join(Program).filter(subscription.c.user == us, subscription.c.program == Program.program_id).all()
   
    print(stmt_user)
    
    
    for sub in stmt_user:
        program_id = sub.program
        
        query_result = db.session.query(Stage.stage_name,Stage.start,Stage.end,Event.event_description).join(Event).join(Program).\
        filter(Program.program_id == program_id).all()
        result_dict = {}    
        result =convert(query_result,result_dict)
       
        print(result)
        age = sub.age
        for stage,event in result.items():
            if stage[1] == age or  stage[2] == age or (stage[1] + 1) ==age or stage[2] + 1 == age:
                
                events = event
        print(events)
        print(query_result)
        # print(program_id)
                
    return redirect(url_for('user_management.display_notifications', result=result))
    
    # return redirect(url_for('user_management.display_notifications',events = events, program = program) )
        
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
@user_management_blueprint.route('/display_notifications/<result>' ,methods=['GET','POST'])

def display_notifications(result):
    
    
    return ('mine')
        
        