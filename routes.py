from flask import Flask, render_template, request, flash
from forms import LuggageForm

app = Flask(__name__) 
 
app.secret_key = 'development key'

@app.route('/luggage')
def luggage():
  form = LuggageForm()
  return render_template('luggage.html', form=form)
  
@app.route('/luggage', methods=['GET', 'POST'])
def luggage():
  form = LuggageForm()
 
  if request.method == 'POST':
   if form.validate() == False:
      flash('All fields are required.')
      return render_template('luggage.html', form=form)
   else:
    return 'Entry Submitted to Luggage Log.'
 
  elif request.method == 'GET':
    return render_template('luggage.html', form=form)  
  
