from wtforms import Form, StringField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired
class LuggageForm(Form):
  name = StringField("Last Name", [validators.Required("Please enter a Last Name")])
  ticket = StringField("Ticket #", [validators.Required("Please enter a ticket #")])
  location = StringField("Location", [validators.Required("Please enter a location")])
  bagCount = StringField("Bag Count", [validators.Required("Please enter # of bags")])
  loggedIn = StringField("Logged By", [validators.Length(min=2, max=3, message='Please enter your initals, only 2 or 3 letters')])
  submit = SubmitField("Store")

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
