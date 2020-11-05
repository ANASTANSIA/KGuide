from app import app, db,login
from flask import render_template,redirect
from flask import flash, url_for
from flask_login import login_user, logout_user, current_user
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from app.models import Product, User

from urllib import request
from werkzeug.exceptions import abort
from werkzeug.urls import url_parse
from _datetime import datetime
from app.products.forms import EmptyForm
from app.user import user_blueprint

# @app.before_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.utcnow()
#         db.session.commit()


    # user profile //details
@user_blueprint.route('/user/<username>')
#@login_required   
def user(username):
    
    user = User.query.filter_by(username=username).first_or_404()
   #products posted by the user
    page = request.args.get('page',1,type=int)
    products = user.products.order_by(Product.timestamp.desc()).paginate(page, app.config['POST_PER_PAGE'], False)
    
    next_url = url_for('user', username=user.username,products=page.products.next_num)\
        if products.has_next else None
        
    prev_url = url_for('user', username=user.username,products=page.products.prev_num)\
        if products.has_prev else None
       
    form = EmptyForm()
        
    return render_template('user.html',user=user,products=products,next_url=next_url,prev_url=prev_url)
       

    return render_template('user.html',user=user)


@user_blueprint.route('/edit_profile',methods=['GET','POST'])
#@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your profile has been updated!')
        return redirect(url_for('user.edit_profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html',form=form)


@user_blueprint.route('/delete_product')
# @login_required
def delete_product(product):
    productResult= Product.query.filter_by(Product.product_id == product)
    db.session.delete(productResult)
    db.session.commit()
    return redirect(url_for('user.user/<username>'))
