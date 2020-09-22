# stores web form classes
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField,  PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from wtforms.fields.simple import TextAreaField



class EditProfileForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    about_me = TextAreaField('About Me',validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username,*args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_on_submit(self,username):
        if username.data !=self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')
        return super().validate_on_submit()

