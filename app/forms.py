from wtforms import Form, StringField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired
from models import Luggage

def already_exists(form, field):
    if Luggage.query.filter_by(ticket=field.data).first():
        raise ValidationError('This ticket already exists')

class LuggageForm(Form):
  name = StringField("Last Name", [validators.Required("Please enter a Last Name"), validators.Regexp(r"[A-Za-z-\']+", message="Please include only letters")])
  ticket = StringField("Ticket #", [validators.Required("Please enter a ticket #"), already_exists])
  location = StringField("Location", [validators.Required("Please enter a location")])
  bagCount = StringField("Bag Count", [validators.Required("Please enter # of bags"), validators.Regexp(r"\d{1,2}$", message="Please include only numbers. Maximum of two digits.")])
  loggedIn = StringField("Logged By", [validators.Length(min=2, max=3, message='Please enter your initals, only 2 or 3 letters')])
  submit = SubmitField("Store")

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
