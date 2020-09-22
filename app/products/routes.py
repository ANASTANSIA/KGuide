
from app import db
from app.models import Product
from app.products.forms import ProductForm
from werkzeug.utils import redirect, secure_filename
import os
import app
from fileinput import filename
from urllib import request
from flask.helpers import flash, send_from_directory, url_for
from flask.templating import render_template
from app.products import product_blueprint
from os import path





def allowed_file(filename):
    
    return '.' in filename and \
        filename.rsplit('.,1')[1].lower()

           
@product_blueprint.route('/upload_product', methods=['POST','GET'])
#@login_required

def add_product():
    
    form = ProductForm()
    image = form.image_path.data
    if allowed_file(image.filename):
        
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.Config['UPLOAD_FOLDER'], filename))
        image_path = image.save(os.path.join(app.Config['UPLOAD_FOLDER'], filename))
        
    if form.validate_on_submit():
    
        product = Product(product_type=form.product_type.data,quantity=form.product_quantity.data,product_description=form.product_description.data,image_path=image_path)
        db.add(product)
        db.commit()
        flash('Product Added Successfully!')
    else:
        flash('Error in adding your product!') 
           
    return render_template('products/products.html',form=form)   


        
@product_blueprint.route('/view_product')
def view_product():
    productswithImage = []
    page = request.args.get('page',1,type=int)
    product_result =Product.query.order_by(Product.timestamp.desc()).paginate(page, app.config['POST_PER_PAGE'],False)
    
    for product in product_result:
       image = download_image(product.image_path)
       productswithImage.append(product.product_type, product.product_quantity,product.product_description,image)
    
    next_url = url_for('view_product',page=productswithImage.next_num)\
        if productswithImage.has_next else None
        
    prev_url = url_for('view_product', page=productswithImage.prev_num)\
        if productswithImage.has_prev else None
        
    return render_template('products/products.html', products=productswithImage.items, next_url=next_url, prev_url=prev_url)
    

    return render_template('products/products.html',products=productswithImage.items)

#getting image from folder
def download_image(image_path):
    
    return send_from_directory(app.Config.UPLOAD_FOLDER,path,as_attachment=True)

def search():
    
    return('Result')


def delete_product(product_id):

    
    return render_template("products/products.html")