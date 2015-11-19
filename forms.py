from flask.ext.wtf import Form, TextField, SubmitField, validators, ValidationError
 
class LuggageForm(Form):
  name = TextField("Last Name", [validators.Required()])
  ticket = TextField("Ticket #", [validators.Required()])
  location = TextField("Location", [validators.Required()])
  bagCount = TextAreaField("Bag Count", [validators.Required()])
  submit = SubmitField("Store")
