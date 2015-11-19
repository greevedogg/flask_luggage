from flask import Flask, render_template, request
from forms import LuggageForm

app = Flask(__name__) 
 
app.secret_key = 'development key'

@app.route('/luggage')
def luggage():
  form = LuggageForm()
  return render_template('luggage.html', form=form)
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    return 'Form posted.'
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form)  
  
