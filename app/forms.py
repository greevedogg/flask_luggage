from wtforms import Form, TextField, SubmitField, validators, ValidationError

class LuggageForm(Form):
  name = TextField("Last Name", [validators.Required("Please enter a Last Name")])
  ticket = TextField("Ticket #", [validators.Required("Please enter a ticket #")])
  location = TextField("Location", [validators.Required("Please enter a location")])
  bagCount = TextField("Bag Count", [validators.Required("Please enter # of bags")])
  submit = SubmitField("Store")
