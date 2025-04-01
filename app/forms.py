from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class FindItemForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")


class BorrowForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired(), NumberRange(min=1)])
    iid = IntegerField("Item ID", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Borrow Item")
    

class ReturnForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    iid = IntegerField("Item ID", validators=[DataRequired()])
    submit = SubmitField("Return")
    
    
class DonateForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    item_type = StringField("Type", validators=[DataRequired()])
    submit = SubmitField("Donate")
    

class FindEventForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")
    

class RegisterEventForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    eid = IntegerField("Event ID", validators=[DataRequired()])
    submit = SubmitField("Register")
    

class VolunteerForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    hours = IntegerField("Hours to add", validators=[DataRequired()])
    submit = SubmitField("Volunteer")
    

class HelpForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    submit = SubmitField("Ask for Help")