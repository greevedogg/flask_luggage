from flask.ext.wtf import Form, TextField, SubmitField
 
class LuggageForm(Form):
  name = TextField("Last Name")
  ticket = TextField("Ticket #")
  location = TextField("Location")
  bagCount = TextAreaField("Bag Count")
  submit = SubmitField("Store")
