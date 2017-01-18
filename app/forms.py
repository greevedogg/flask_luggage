from wtforms import Form, StringField, TextAreaField, SubmitField, HiddenField, validators, ValidationError
from wtforms.validators import DataRequired
from models import Luggage
from string import lower
import re

def already_exists(form, field):
    if not form.id.data and Luggage.query.filter_by(ticket=field.data).first():
        raise ValidationError('This ticket already exists. Please use a new ticket number.')


def check_last_modified(form, field):
    if form.id.data and not 2 <= len(field.data) <= 3:
        raise ValidationError('Please enter your initials, only 2 or 3 letters')


def check_location(form, field):
    exceptionsAllowed = ["corral", "cart", "desk"]
    if exceptionsAllowed.count(lower( field.data )) == 0 and not re.search("^[0-9]+[A-Za-z-\']+$", field.data):
        raise ValidationError('Location has to start with numbers and ends with letters. Exceptions: Corral, Cart, Desk')


class LuggageForm(Form):
  name = StringField("Last Name", [validators.Required("Please enter a Last Name"), validators.Regexp(r"[A-Za-z-\']+", message="Please include only letters")])
  ticket = StringField("Ticket #", [validators.Required("Please enter a Ticket #"), already_exists])
  location = StringField("Location", [validators.Required("Please enter a Location"), check_location])
  # bagCount = StringField("Bag Count", [validators.Required("Please enter # of bags"), validators.Regexp(r"\d{1,2}$", message="Please include only numbers. Maximum of two digits.")])
  bagCount = StringField("Bag Count", [validators.Required("Please enter # of Bags")])
  comments = TextAreaField("Comments")
  loggedInBy = StringField("Logged By", [validators.Length(min=2, max=3, message='Please enter your initials, only 2 or 3 letters')])
  modifiedBy = StringField("Last Modified By", [check_last_modified])
  submit = SubmitField("Store")
  id = HiddenField("Id")

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
