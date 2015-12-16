from wtforms import Form, StringField, SubmitField, validators, ValidationError

class LuggageForm(Form):
  name = StringField("Last Name", [validators.Required("Please enter a Last Name")])
  ticket = StringField("Ticket #", [validators.Required("Please enter a ticket #")])
  location = StringField("Location", [validators.Required("Please enter a location")])
  bagCount = StringField("Bag Count", [validators.Required("Please enter # of bags")])
  submit = SubmitField("Store")

class SearchForm(Form):
    search = StringField('search', [validators.Required('Please enter a Last Name or Ticket #')])
