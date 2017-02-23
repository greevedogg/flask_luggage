from wtforms import Form, StringField, TextAreaField, SubmitField, HiddenField, validators, ValidationError, PasswordField
from wtforms.validators import DataRequired
from models import Luggage, User
from string import lower
import re
from flask_wtf.file import FileField

def already_exists(form, field):
    if not form.id.data and Luggage.query.filter_by(ticket=field.data).first():
        raise ValidationError('This ticket already exists. Please use a new ticket number.')


def check_last_modified(form, field):
    if form.id.data and not 2 <= len(field.data) <= 3:
        raise ValidationError('Please enter your initials, only 2 or 3 letters')


def check_location(form, field):
    exceptionsAllowed = ["corral", "cart", "desk", "ref"]
    if exceptionsAllowed.count(lower( field.data )) == 0 and not re.search("^[0-9]+[A-Za-z-\']+$", field.data):
        raise ValidationError('Location has to start with numbers and ends with letters. Exceptions: Corral, Cart, Desk, Ref')


def valid_credentials(form, field):
    if not form.username.data or not form.password.data:
        raise ValidationError('Both fields are required.')
    if User.query.filter_by(username=form.username.data, password=form.password.data).first() is None:
        raise ValidationError('User not found with this username and password.')
    if form.currentHotel:
        u = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if u is not None and u.hotel.name != form.currentHotel:
            raise ValidationError('User does not belong to %s Hotel.' % form.currentHotel)
    
    
    


def check_current_password(form, field):
    if field.data != form.currentPassword:
        raise ValidationError('Invalid current password')


def check_password(form, field):
    if len(field.data) < 6:
        raise ValidationError('Password should have least 6 characters')
    if form.password1.data != form.password2.data:
        raise ValidationError('Both passwords are not identical')


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


class LoginForm(Form):
    username = StringField('Username', validators=[validators.Required("Please enter a Username"), validators.Regexp(r"[A-Za-z-\']+", message="Please include only letters")])
    password = PasswordField("Password", validators=[validators.Required("Please enter the password"), valid_credentials])
    def __init__(self, formdata=None, *args, **kwargs):
        super(LoginForm, self).__init__(formdata, *args, **kwargs)
        self.currentHotel = args[0]


class ChangePasswordForm(Form):
    current = PasswordField('Current Password', validators=[validators.Required("Please enter the current password"), check_current_password])
    password1 = PasswordField("New Password", validators=[validators.Required("Please enter the new password"), check_password])
    password2 = PasswordField("Confirm Password", validators=[validators.Required("Please enter the password again"), ])
    def __init__(self, formdata=None, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(formdata, *args, **kwargs)
        self.currentPassword = args[0]
        


class HotelForm(Form):
    name = StringField('Name', validators=[validators.Required("Please enter a name"), validators.Regexp(r"[A-Za-z-\']+", message="Please include only letters")])
