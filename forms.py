
from wtforms.fields.core import IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProgramForm(FlaskForm):
    program_name = StringField('Program Name', validators=[DataRequired()])
    program_description = TextAreaField('Program Description',validators=[Length(min=0,max=140)])
    submit = SubmitField('Create a Program')
    
    
    def validate(self,program_name):
        
        return super().validate()


class StageForm(FlaskForm):
    
    stage_name = StringField('Stage Name',validators=[DataRequired()])
    start = IntegerField('Start Age in Days',validators=[DataRequired()])
    end = IntegerField('End Age in Days',validators=[DataRequired()])
    event_description = StringField('Event Description',validators=[DataRequired()])
    
    submit = SubmitField('Submit')
    
