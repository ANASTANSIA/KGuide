
from flask import flash, send_from_directory, url_for,request,current_app,request,g
from fileinput import filename
from flask.templating import render_template
from app.products import product_blueprint
from flask_login import current_user, login_required
import os
from os import path
from app import db
from app.models import Comment, Product

from werkzeug.utils import redirect, secure_filename

import app
import imghdr
import datetime
from app.products.forms import SearchForm


   




def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None,header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

# def allowed_file(filename):
    
#     return '.' in filename and \
#         filename.rsplit('.,1')[1].lower() in current_app.Config['ALLOWED_EXTENSIONS']

           
@product_blueprint.route('/add_product', methods=['POST','GET'])
@login_required

def add_product():
           
    return render_template('products/create_product.html') 
  
@product_blueprint.route('/addd_product', methods=['POST','GET'])
@login_required
def addd_product():
    if request.method == "POST":
        request_data = request.form
        product_type = request_data.get("product_type")
        quantity = request_data.get("quantity")
        product_description =request_data.get("product_description")
        
        image = request.files.get("image")
        filename = secure_filename(image.filename)
        if filename !='':
            file_extension = os.path.splitext(filename)[1]
            if file_extension not in current_app.config['ALLOWED_EXTENSIONS'] or \
                file_extension != validate_image(image.stream):
                    flash("no image file")
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
            image_path = image.filename
            
            print(image_path)

    
            product = Product(product_type=product_type,quantity=quantity,product_description=product_description,image_path=image_path,user_id = current_user.id)
            print(product)
           
            db.session.add(product)
            db.session.commit()
            flash('Product Added Successfully!')
        else:
           flash('Error in adding your product!') 
        
        
    
    
    return redirect(url_for('products.view_product'))
   # return render_template('products/products.html')
        
@product_blueprint.route('/view_product', methods=['GET','POST'])
@login_required
def view_product():
    # return 'View product Page'
    
    page = request.args.get('page',1,type=int)
    product_result =Product.query.order_by(Product.timestamp.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    print(product_result)
    next_url = url_for('view_product',page=product_result.next_num)\
         if product_result.has_next else None
        
    prev_url = url_for('view_product', page=product_result.prev_num)\
         if product_result.has_prev else None  
     
    return render_template('products/products.html',product_result= product_result.items, next_url=next_url, prev_url=prev_url)
    

    # return render_template('products/products.html',products=productswithImage.items)
    
    

#getting image from folder
@product_blueprint.route('/download_image/<image_path>')
def download_image(image_path):
    # 
    # return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER']),image_path,as_attachment=True)
    return redirect(url_for('static',filename='uploads/' +image_path), code=301)

@product_blueprint.route('/search')
@login_required
def search():
    
    if not g.search_form.validate():
        return redirect(url_for('product_blueprint.view_product'))
    page = request.args.get('page', 1, type=int)
    posts, total = Product.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('product_blueprint.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('product_blueprint.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', posts=posts, next_url=next_url, prev_url=prev_url)
                       
 

 ######WORK ON COMMENTING   
@product_blueprint.route('/comment_product/<product_id>/<comment_id>',methods=['GET','POST'])
@login_required  
   
def comment_product(product_id,comment_id=0):
    product = Product.query.get_or_404(product_id)
    comment_id = Comment.query.get_or_404(id)
    comments = Comment.query.order_by(Comment.timestamp.desc().all)
    if request.method == 'POST':
        req = request.form
        text = req.get('comment')
        
        comment =Comment(text=comment,author=current_user.id,parent_id=Comment.id,product_id=Product.product_id)
        comment.save()
        
    
            
    
    # result = Comment.query.order_by(Comment.path)
    return render_template('Products/comment.html',comments=comments,product=product)

@product_blueprint.route('/comment/<product_id>/<comment_id>',methods=['GET','POST'])
def comment(product_id,comment_id=0):
    
    return render_template('products/comment.html',product_id=product_id,comment_id=comment_id)
        