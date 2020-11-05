from app.user_management import user_management_blueprint
from app.models import Event, Program, Stage
from app import app, db,login
from flask import request
from flask_login import current_user

from sqlalchemy.orm import session


@user_management_blueprint.route('/subscribe/<program_id>' ,methods=['GET','POST'])
def subscribe(program_id):
    if request.method == "POST":
        age = request.form.get('age')
        # subscription = Subscription(age = age,program_id = program_id,activated=True ,user_id = current_user.id)
        
        # db.session.add(subscription)
        # db.session.commit()
    
    return ('subscribed!!!')


# def get_subscriptions():
    # subscriptions = Subscription.query.all()
    # program = subscriptions.program_id
    # age = subscriptions.age
    # for subscription in subscriptions:
        
    #     if subscriptions.activated == True:
            
    #         query = db.session.query(Stage.stage_name,Stage.start,Stage.end,Event.event_description).join(Event).join(Program).\
    #         filter(Program.program_id == program).all()
            
    #         print(query)
            
    #     result_dict = {}    
    #     result =convert(query,result_dict)  

        
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
        
        