from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import IntegerField, SelectField, SubmitField, TextAreaField, TextField

from wtforms.validators import Length

class ProductForm(FlaskForm):
    product_type = SelectField('Product Type', choices=[('Eggs','Eggs'),('Chicks','Chicks'),('Broilers','Broilers'),('Layers','Layers')])
    quantity = IntegerField('Quantity')
    product_description = TextAreaField('About Me',validators=[Length(min=0,max=140)])
    image_path = FileField('Image',validators=[FileRequired(),FileAllowed(['jpg','png'],'An Image is Required')])
    submit = SubmitField('Post')
    
class EmptyForm():
    submit = SubmitField('Submit')