from datetime import datetime

from flask_apscheduler import APScheduler

from app import db
from app.models import Subscriptions

scheduler = APScheduler()


def age_incrementer():
    utc_now = datetime.utcnow()
    print(utc_now)
    app = scheduler.app
    with app.app_context():
        subscriptions = Subscriptions.query.all()
        for subscription in subscriptions:
            try:
                if subscription.age:
                    sub_day = subscription.subscription_day
                    age_difference = utc_now - sub_day
                    
                    if (age_difference.hours) >= 24:
                        new_age = age_difference.hours // 24 
                        subscription.age = new_age
                        
                    elif(age_difference.hours) == 24:
                        new_age = subscription.age
                        new_age += 1
                        subscription.age = new_age
                    else:
                        new_age = subscription.age
                        subscription.age = new_age
                else:
                    new_age = 1
                    subscription.age = new_age
                    
                        
                    
            except Exception as e:
                print(str(e))
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
    return ('age incremented')